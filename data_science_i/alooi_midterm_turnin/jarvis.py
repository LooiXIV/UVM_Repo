#!/usr/bin/env python
# -*- coding: utf-8 -*-

# jarvis.py
# Alooi
import websocket
import pickle
import json
import urllib
import requests
import sqlite3
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline as pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import preprocessing
# you can import other sklearn stuff too!
# FILL IN ANY OTHER SKLEARN IMPORTS ONLY

import botsettings # local .py, do not share!!
TOKEN = botsettings.API_TOKEN
DEBUG = True

def debug_print(*args):
    if DEBUG:
        print(*args)


try:
    conn = sqlite3.connect("jarvis.db")
except:
    debug_print("Can't connect to sqlite3 database...")


def post_message(message_text, channel_id):
    requests.post("https://slack.com/api/chat.postMessage?token={}&channel={}&text={}&as_user=true".format(TOKEN,channel_id,message_text))


class Jarvis():
    
    def __init__(self): # initialize Jarvis
        self.JARVIS_MODE = None
        self.ACTION_NAME = None
        
        # SKLEARN STUFF HERE:
        # load in old documents/old memory
        jarv_mem = conn.cursor()
        doc = []
        lab = []
        for row in jarv_mem.execute("SELECT * from training_data"):
            doc.append(row[1])
            lab.append(row[2])
        self.memory = {'document':doc,'label': lab}
        self.BRAIN = pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer()),
                        ('clf', MultinomialNB()),])

    def on_message(self, ws, message):
        m = json.loads(message)
        print('####################DEBUG PRINT####################', '\n')
        debug_print(m, self.JARVIS_MODE, self.ACTION_NAME)
        print('\n', '####################DEBUG PRINT####################')

        # only react to Slack "messages" not from bots (me):
        if m['type'] == 'message' and 'bot_id' not in m:
            print('\n')
            print('detected message')
            print('\n')

            # put into training mode
            if m['text'].lower() == 'training time':
                print('\n')
                print('Going into training mode')
                print('\n')

                response = 'Ready for training'
                self.JARVIS_MODE = 'training'
                post_message(response, m['channel'])
                response = 'What is the CORPUS type?'
                post_message(response, m['channel'])

            # put into testing mode
            elif m['text'].lower() == 'testing time':
                print('\n')
                print('Going into testing mode')
                print('\n')

                if bool(self.memory['document']) == True:
                    self.BRAIN.fit(self.memory['document'], self.memory['label'])
                    response = 'Ready for testing, what is the phrase for testing?'            
                    self.JARVIS_MODE = 'testing'
                    # fit the model once we're in testing mode

                else:
                    response = 'I have not been trained yet! Train me first!'
                    print('\n')
                    print('Not in testing mode')
                    print('\n')

                post_message(response, m['channel'])

            # get testing phrases and test the phrases
            elif self.JARVIS_MODE == 'testing':
                print('\n')
                print('Getting testing phrases from user')
                print('\n')

                if m['text'].lower() == 'finished with testing':
                    self.JARVIS_MODE = None
                    self.ACTION_NAME = None
                    response = 'Alright, done with testing'
                    post_message(response, m['channel'])

                else:
                    test_phrase = [m['text']]
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print(test_phrase)
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    phrase_pred = self.BRAIN.predict(test_phrase)
                    response = 'This phrase is part of category {}'.format(phrase_pred[0].upper())
                    post_message(response, m['channel'])
                    response = 'Are there more phrases to test?'
                    post_message(response, m['channel'])

            # in training mode, need to select ACTION_NAME
            elif self.JARVIS_MODE == 'training' and self.ACTION_NAME == None:
                print('\n')
                print('Getting action name from user')
                print('\n')
                
                self.ACTION_NAME = m['text'].lower()
                response = 'Ok, what text should I associate with {}?'.format(self.ACTION_NAME)
                post_message(response, m['channel'])

            # once an ACTION_NAME is selected build the training corpus with
            # text typed through slack.
            elif self.JARVIS_MODE == 'training' and self.ACTION_NAME != None:
                print('\n')
                print('Getting words to associate with {} from user'.format(self.ACTION_NAME))
                print('\n')

                # if the word phrase is 'finished training exit training mode'
                # thus set the mode and action name to 'none'.
                # build the model for the brain, pickle and save the model
                # finally store the data in the sqlite data base
                if m['text'].lower() == 'finished with training':
                    self.JARVIS_MODE = None
                    self.ACTION_NAME = None
                    response = 'Alright, done training'
                    post_message(response, m['channel'])
                    
                    # now actually train the model
                    X_train = self.memory['document']
                    Y_train = self.memory['label']
                    self.BRAIN.fit(X_train, Y_train)
                    
                    # save the newly trained model
                    save_brain = open('jarvis.pkl', 'wb')
                    pickle.dump(self.BRAIN, save_brain)
                    save_brain.close()

                else:
                                       # save the new training data to the database
                    jarv_mem = conn.cursor()
                    jarv_mem.execute("INSERT INTO training_data (txt,action) VALUES (?, ?)", (m['text'], self.ACTION_NAME,))
                    conn.commit()
                    print(m['text'], self.ACTION_NAME)
                    self.memory['label'].append(self.ACTION_NAME) 
                    self.memory['document'].append(m['text'])
                    response = 'Okay, are there more training phrases?'
                    post_message(response, m['channel'])
                    print('\n')
                    print(self.memory)
                    print('\n')




def start_rtm():
    """Connect to Slack and initiate websocket handshake"""
    r = requests.get("https://slack.com/api/rtm.start?token={}".format(TOKEN), verify=False)
    r = r.json()
    r = r["url"]
    return r


def on_error(ws, error):
    print("SOME ERROR HAS HAPPENED", error)


def on_close(ws):
    conn.close()
    print("Web and Database connections closed")


def on_open(ws):
    print("Connection Started - Ready to have fun on Slack!")


r = start_rtm()
jarvis = Jarvis()
ws = websocket.WebSocketApp(r, on_message=jarvis.on_message, on_error=on_error, on_close=on_close)
ws.run_forever()


