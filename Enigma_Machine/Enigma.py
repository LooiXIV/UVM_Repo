#!/anaconda3/bin/env python3
# -*-utf-8-*-

# Rotor class 
class rotors(object):
    def __init__(self):
        # the default alphabet
        self.alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        # match the default alphabet to a sequence of numbers
        self.alph_num = range(0, len(self.alphabet))
        # dictionary of a single rotor
        self.rotor = {'name': None, 
                'init_set': 0, 
                'encoding': self.alphabet, 
                'turn_count': 0,
                'full_turn': False}
 
    # set the encoding of the rotor
    def init(self, encoding=None, name=None):
        '''Initialize a rotor encoding'''
        if name == None:
            print('please name the rotor')
        elif encoding == None:
            print('please select an encoding for the rotor')
        else:
            self.rotor['encoding'] = list(encoding)
            self.rotor['name'] = name
    
    def info(self):
        '''Prints the info of a rotor:
           1) name of the rotor
           2) the initial dial setting
           3) the enconding of the rotor
           4) the number of turns the rotor has made'''
        for i in self.rotor.keys():
            print(i+': ', self.rotor[i])

    def turn(self):
        self.rotor['turn_count'] += 1

        if self.rotor['full_turn'] == True:
            self.rotor['full_turn'] = False

        if self.rotor['turn_count'] > 25:
            self.rotor['turn_count'] = 0
            self.rotor['full_turn'] = True

    def reset(self):
        self.rotor['turn_count'] = 0

# machine encoder and decoder
class enig_machine(object):

    def __init__(self):
        # default plug board setting
        self.reflector = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'

        self.plug_b = ['AA', 'BB', 'CC', 'DD', 'EE',
                'FF', 'GG', 'HH', 'II', 'JJ']
        self.rotor_setting = {1:None, 2:None, 3:None}

    def install_rotor(self, rotor=None, pos=None):
        '''installs a rotor at the position specified'''
        if pos > 3 or pos < 1:
            print('"pos" needs to be an integer greater than 0 and less than 3')
        elif type(rotor) is not rotors:
            print('"rotor" does not appear to be type "rotor"')
        else:
            self.rotor_setting[int(pos)] = rotor

    # set the plug board setting for extra scrambling.
    def set_plug_board(plug_board=['AA', 'BB', 'CC', 'DD', 'EE',
                'FF', 'GG', 'HH', 'II', 'JJ']):
        '''Set the plug board for additional scrambling, 
        If this is not specified then there is not scrambling'''
        self.plug_b = plug_board

    def machine_settings(self):
        '''show the settings for the machine'''
        print('Plug Board Settings')
        print(self.plug_b)
        for n, r in enumerate(self.rotor_setting.keys()):
            print('#'*60)
            print('Rotor'+str(n+1), self.rotor_setting[r].info())
        
    # Remove the rotors installed in the
    # enigma machine
    def remove_rotors(self):
        '''Removes all rotors in the machine'''
        self.rotor_setting = {1:None, 2:None, 3:None}

    def install_reflector(self, reflector='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        '''Set the reflector, the default is the alphabet in order'''
        self.reflector = reflector

    # encode the message with a function that 
    def encode_decode(self, message, initial=[0,0,0]):
        alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        coded_msg = []
        
        # set the initial rotor settings for the enigma machine
        # set the first rotor
        self.rotor_setting[1].rotor['init_set'] = initial[0]
        self.rotor_setting[1].rotor['turn_count'] = initial[0]
        # set the second rotor
        self.rotor_setting[2].rotor['init_set'] = initial[1]
        self.rotor_setting[2].rotor['turn_count'] = initial[1]
        # set the second rotor
        self.rotor_setting[3].rotor['init_set'] = initial[2]
        self.rotor_setting[3].rotor['turn_count'] = initial[2]


        # remove the spaces
        no_space_msg = ''.join(message.upper().split(' '))
        # seperate each letter
        list_msg = list(no_space_msg)
        
        # set the plug board
        plug_b = self.plug_in

        # go through the rotors
        for t, l in enumerate(list_msg):

            # go through the plug board
            pb_l = [list(p)[1][0] for p in plug_b if l == list(p)[0][0]]

            # Turn and go through the first rotor
            self.rotor_setting[1].turn()
            l_index1 = alphabet.index(pb_l[0])
            a1 = self.rotor_setting[1].rotor['encoding'][l_index1]
            
            # if the first rotor goes through a full turn, turn the
            # second rotor, then go through the second rotor
            if self.rotor_setting[1].rotor['full_turn']:
                self.rotor_setting[2].turn()
                #print('rotor 2 turn')
            l_index2 = alphabet.index(a1)
            a2 = self.rotor_setting[2].rotor['encoding'][l_index2]


            # if the second rotor goes through a full turn, turn the
            # second rotor, then go through the second rotor
            if self.rotor_setting[2].rotor['full_turn']:
                self.rotor_setting[3].turn()
                #print('rotor 3 turn')

            l_index3 = alphabet.index(a2)
            a3 = self.rotor_setting[3].rotor['encoding'][l_index3]

            # go through the reflector board
            r_index = self.reflector.index(a3)
            ar = alphabet[r_index]

            # go back through the rotors
            l_index4 = self.rotor_setting[3].rotor['encoding'].index(ar)
            a4 = alphabet[l_index4]

            l_index5 = self.rotor_setting[2].rotor['encoding'].index(a4)
            a5 = alphabet[l_index5]

            l_index6 = self.rotor_setting[1].rotor['encoding'].index(a5)
            a6 = alphabet[l_index6]
            
            # go through the plug board again
            pb_l2 = [list(p)[1] for p in plug_b if a6 == list(p)[0]]

            
            # add the encrypted letter to the coded message
            coded_msg.append(pb_l2[0])
        # return the encrypted or decrypted message
        return ''.join(coded_msg)

# A set of rotors that were used by the Germans in WWII
class rotor_sets(object):
    def __init__(self):

        self.I_K = ['I_K', 'PEZUOHXSCVFMTBGLRINQJWAYDK']

        self.II_K = ['II_K', 'ZOUESYDKFWPCIQXHMVBLGNJRAT']

        self.III_K = ['III_K', 'EHRVXGAOBQUSIMZFLYNWKTPDJC']

        self.UKW_K = ['UKW_K', 'IMETCGFRAYSQBZXWLHKDVUPOJN']

        self.ETW_K = ['ETW_K', 'QWERTZUIOASDFGHJKPYXCVBNML']

# Sets of reflectors used by the Germans in WWII
class reflectors_sets(object):
    def __init__(self):

        self.Reflector_B = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
        self.Reflector_C = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
        self.Reflector_B_Thin = 'ENKQAUYWJICOPBLMDXZVFTHRGS'
        self.Reflector_C_Thin = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'


class plug_board_sets(object):
    def __init__(self):
        self.PB = ['AP', 'BX', 'CQ', 'DR', 'EO', 'FH', 'GT', 'UZ', 'IY', 'JS']
