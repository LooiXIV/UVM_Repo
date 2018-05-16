#!/anaconda3/bin/env python3
# -*-utf-8-*-

'''
Authors: Alexander Looi, LooiXIV@gmail.com; Andrew Metcalf, aametcalf01@gmail.com; David Landay, davidlanday@gmail.com


Code to train the CNN-LSTM model with the Brats 2017 Data. To run this code simply call $python CNN_RNN_Brats17.py. Training data needs to be in a directory labelled Brats17TrainingData. Additionally, the training data directory needs to be in a folder called preprocessed. Lastly, each brain needs to be in a 4 dimensional array (if using tensorflow as backend) Where the first dimensions correspondes to the layers of the brain image, the middle two layers are the x and y (columns and rows) of each brain image, and the last layer are the channels (the four modalities/MRI image types).  
'''
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize, downscale_local_mean
from skimage.io import imsave
import PIL
import random
import pandas as pd

from keras.preprocessing.image import ImageDataGenerator
from keras.initializers import glorot_normal
from keras.models import Model, Sequential
from keras.layers import Input, Concatenate, Conv2D, MaxPooling2D, Conv2DTranspose, concatenate, UpSampling2D
from keras.layers import LSTM, RNN, Dense, Flatten, Reshape, TimeDistributed, ConvLSTM2D, Dropout
from keras.regularizers import l2, l1
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import keras.backend as K

#from keras import backend as K
import keras
print(keras.__version__)

# if the directory exists cd into the directory
if os.path.isdir('preprocessed/'):
    os.chdir('preprocessed/Brats17TrainingData')
print(os.getcwd())

# logical to state if to plot or not
to_plot = False 
# hyper parameters defined here
num_epochs = 400
batch_size = 20
steps = 5
# dimensions of our images.
img_cols, img_rows = 96, 96
train_data_dir = 'Brats17TrainingData'
# image depth
img_depth = 155
im_channels = 4


# define the dice loss
def dice_coef(y_true, y_pred):
    smooth = 1.
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)

# In the case of a list of files. Define the data generator to feed data to train the model. 
def data_gen(x, y, batch_size, num_steps, LW_size=(96, 96), vid_len=155, n_channels=1, val_split=0.2, for_val=False):
    """Data Generator to feed data into the model for training.""" 
    x_array = np.asarray(x)
    y_array = np.asarray(y)
    tot_num_data = len(x) 
    
    # find the number of files for the training and validation set
    if for_val:
        num_choices = int(val_split*tot_num_data)
    else:
        num_choices = int((1-val_split)*tot_num_data)

    # randomly choose files for either the validation or training set
    data_choice = np.asarray(random.sample(list(np.arange(0,tot_num_data)), num_choices))

    # get the training files, and the truth files
    x_choices = x_array[data_choice]
    y_choices = y_array[data_choice]
    
    while True:
        # loop through all the x_choices.
        for i in range(len(x_choices)):
            raw_vid = np.load(x[i])
            raw_label = np.load(y[i])
            
            # normalize the data from 0 to 1
            norm_vid = raw_vid/np.max(raw_vid)
            
            # get the vid data and the label data
            vid = np.asarray([resize(im, (LW_size[0], LW_size[1], 4)) for im in norm_vid[:,]])
            label = np.asarray([resize(im, (LW_size[0], LW_size[1], 1)) for im in raw_label[:,]])
            
            for j in range((len(vid)-num_steps)//batch_size):
                x_batch, y_batch = [], []
                
                for k in range(batch_size):
                    
                    x_batch.append(vid[j+k:j+k+steps,])
                    y_batch.append(label[j+k:j+k+steps,])
                x_batch, y_batch = np.asarray(x_batch), np.asarray(y_batch)

                yield x_batch, y_batch
                
# Define the model
def get_RNN_UNET(img_rows, img_cols, img_depth, img_channels):
    
    # find where the channels should be defined in the input layer.
    if K.image_data_format() == 'channels_first':
        input_shape = (img_depth, img_channels, img_cols, img_rows)
        print('channels are first')
    else:
        input_shape = (None, img_cols, img_rows, img_channels)
        print('channels are last')

    print('Input Shape: ', input_shape)
    
    # define the inputs for the input layer
    inputs = Input(shape=input_shape)
    
    # Encoder layer 1
    conv11 = TimeDistributed(Conv2D(64, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(inputs)
    print("conv11: ", conv11.shape)
    conv12 = TimeDistributed(Conv2D(64, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv11)
    print("conv12: ", conv12.shape)
    pool1 = TimeDistributed(MaxPooling2D(pool_size=(2,2)))(conv12)
    print("pool1: " , pool1.shape)
    print()

    # Encoder layer2
    conv21 = TimeDistributed(Conv2D(128, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(pool1)
    print("conv21: ", conv21.shape)
    conv22 = TimeDistributed(Conv2D(128, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv21)
    print("conv22: ", conv22.shape)
    pool2 = TimeDistributed(MaxPooling2D(pool_size=(2,2)))(conv22)
    print("pool2: ", pool2.shape)
    print()

    # Encoder layer 3
    conv31 = TimeDistributed(Conv2D(256,(3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(pool2)
    print("conv31: ", conv31.shape)
    conv32 = TimeDistributed(Conv2D(256,(3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv31)
    print("conv32: ", conv32.shape)
    pool3 = TimeDistributed(MaxPooling2D(pool_size = (2,2)))(conv32)
    print("pool3: ", pool3.shape)
    print()

    # Encoder layer 4
    conv41 = TimeDistributed(Conv2D(512,(3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(pool3)
    print("conv41: ", conv41.shape)
    conv42 = TimeDistributed(Conv2D(512,(3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv41)
    print("conv42: ", conv42.shape)
    pool4 = TimeDistributed(MaxPooling2D(pool_size = (2,2)))(conv42)
    print("pool4: ", pool4.shape)
    print()

    # Encoder layer 5
    conv51 = TimeDistributed(Conv2D(1024,(3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(pool4)
    print("conv51: ",conv51.shape)
    conv52 = TimeDistributed(Conv2D(1024,(3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv51)
    print("conv52: ",conv52.shape)
    drop5 = Dropout(0.5)(conv52)
    print()

    # Decoder layer 6
    conv61 = TimeDistributed(Conv2D(512, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(drop5)
    print('conv61: ', conv61.shape)
    upSamp6 = TimeDistributed(UpSampling2D(size = (2,2)))(conv61)
    print("upSamp6: ", upSamp6.shape)
    merge6 = Concatenate(axis = 4)([pool3, upSamp6])
    print("merge6: ", merge6.shape)
    conv62 = TimeDistributed(Conv2D(512, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(merge6)
    print('conv62: ', conv62.shape)
    conv63 = TimeDistributed(Conv2D(512, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv62)
    print('conv63: ', conv63.shape)
    print()

    # Decoder layer 7
    conv71 = TimeDistributed(Conv2D(256, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv63)
    print('conv71: ', conv71.shape)
    upSamp7 = TimeDistributed(UpSampling2D(size = (2,2)))(conv71)
    print("upSamp7: ", upSamp7.shape)
    merge7 = Concatenate(axis = 4)([pool2, upSamp7])
    print("merge7: ", merge7.shape)
    conv72 = TimeDistributed(Conv2D(256, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(merge7)
    print('conv72: ', conv72.shape)
    conv73 = TimeDistributed(Conv2D(256, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv72)
    print('conv73: ', conv73.shape)
    print()

    # Decoder layer 8
    conv81 = TimeDistributed(Conv2D(128, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv73)
    print('conv81: ', conv81.shape)
    upSamp8 = TimeDistributed(UpSampling2D(size = (2,2)))(conv81)
    print("upSamp8: ", upSamp8.shape)
    merge8 = Concatenate(axis = 4)([pool1, upSamp8])
    print("merge8: ", merge8.shape)
    conv82 = TimeDistributed(Conv2D(128, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(merge8)
    print('conv82: ', conv82.shape)
    conv83 = TimeDistributed(Conv2D(128, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv82)
    print('conv83: ', conv83.shape)
    print()

    # Decoder layer 9
    conv91 = TimeDistributed(Conv2D(64, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv83)
    print('conv91: ', conv91.shape)
    upSamp9 = TimeDistributed(UpSampling2D(size = (2,2)))(conv91)
    print("upSamp9: ", upSamp9.shape)
    merge9 = Concatenate(axis = 4)([conv12, upSamp9])
    print("merge9: ", merge9.shape)
    conv92 = TimeDistributed(Conv2D(64, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(merge9)
    print('conv92: ', conv92.shape)
    conv93 = TimeDistributed(Conv2D(64, (3,3), activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv92)
    print('conv93: ', conv93.shape)
    print('input to recurrent layer')

    # Decoder layer 10
    conv10 = TimeDistributed(Conv2D(32, 3, activation='relu', padding='same', 
        kernel_initializer=glorot_normal()))(conv93)


    print('conv: ', conv10.shape)
        # Recurrent Layer # add a convLSTM
    convlstm1 = ConvLSTM2D(1, 1, activation='softmax', padding='same', return_sequences=True)(conv10)
    print('ConvLSTM: ', convlstm1.shape)


    model = Model(inputs=[inputs], outputs=[convlstm1])
    
    model.compile(optimizer=Adam(lr=1e-4), loss=dice_coef_loss, metrics=[dice_coef, 'accuracy'])

    return model

# This trains from Scratch the vgg16 model
# Build the training method to train the model
def train(img_cols, img_rows, img_depth, im_channels):
    # target image size
    # proportion of data to use for validation
    val_split = 0.2

    print('-'*60)
    print('Creating and compiling model...')
    print('-'*60)
    
    filepath = "CNNLSTM_model.h5"
    model = get_RNN_UNET(img_rows, img_cols, img_depth, im_channels)
    model_checkpoint = ModelCheckpoint(filepath, monitor='acc', save_best_only=True)

    print('-'*60)
    print('Loading training data...')
    print('-'*60)
    #imgs_train, imgs_mask_train = load_train_data()
    
    train_data_dir = 'Brats17TrainingData'
    print('-'*60)
    print('print current directory', os.getcwd())
    if os.path.isdir(train_data_dir):
        os.chdir(train_data_dir)
        
    # get lists of the training data, and masks
    mask_data = glob.glob('*truth_reshape.npy')
    train_data = glob.glob('*all_layers.npy')
    
    len_all_data = len(train_data)
    val_steps = int(val_split*len_all_data)
    print('num. training data: ', len_all_data)
    print('num. mask data: ', len(mask_data))
    
    #def data_gen2(x, y, batch_size, num_steps, xy_size=(96, 96), vid_len=155, n_channels=1):
    train_generator = data_gen(train_data, mask_data, batch_size, steps, 
                              LW_size=(img_rows, img_cols), vid_len=155, n_channels=4, 
                              val_split=val_split, for_val=False)
    
    valid_generator = data_gen(train_data, mask_data, batch_size, steps, 
                              LW_size=(img_rows, img_cols), vid_len=155, n_channels=4, 
                              val_split=val_split, for_val=True)
    print('-'*60)
    print('data generator created')
    print('-'*60)
    print('Fitting model...')
    print('-'*60)
    
    hist = model.fit_generator(train_generator, steps_per_epoch=len(train_data)//batch_size, 
                               epochs=num_epochs, verbose=1, callbacks=[model_checkpoint], 
                               validation_data=valid_generator, validation_steps=val_steps)
    
    return hist

# run the training code and save it.
history = train(img_cols, img_rows, img_depth, im_channels)
print('~fin~') # finished training

if os.path.isdir('Brats17TrainingData') != True:
    os.chdir('../')

# plot the loss and dice coefficients here
dice_train = history.history['dice_coef']
loss_train = history.history['loss']
dice_valid = history.history['val_dice_coef']
loss_valid = history.history['val_loss']
acc_train = history.history['acc']
acc_valid = history.history['val_acc']
err_train = [1-val for val in acc_train]
err_valid = [1-val for val in acc_valid]

# save as a csv
all_data = {'dice_train': dice_train, 'loss_train': loss_train, 
        'dice_valid': dice_valid, 'loss_valid': loss_valid,
        'acc_train': acc_train, 'acc_valid': acc_valid,
        'err_train': err_train, 'err_valid': err_valid}

loss_data = pd.DataFrame.from_dict(all_data)
data_to_write = pd.DataFrame.from_dict(loss_data)
data_to_write.to_csv('loss_data.csv', sep=',')

if to_plot:
    FS = 20 # font size
    # plot the loss
    plt.figure(figsize=(15,10))
    plt.plot(loss_train)
    plt.plot(loss_valid)
    plt.legend(['Training loss', 'Validation loss'], fontsize=FS)
    plt.xlabel('epoch', fontsize=FS)
    plt.ylabel('Dice Loss', fontsize=FS)
    plt.tick_params(axis='both', labelsize=FS-5)
    plt.savefig('LossCNNRNN.png', dpi=600)

    # plot the dice
    plt.figure(figsize=(15,10))
    plt.plot(dice_valid)
    plt.plot(dice_train)
    plt.legend(['dice coef. Training', 'dice coef. Validation'], fontsize=FS)
    plt.xlabel('epoch', fontsize=FS)
    plt.ylabel('Dice Coef.', fontsize=FS)
    plt.tick_params(axis='both', labelsize=FS-5)
    plt.savefig('DiceCNNRNN.png', dpi=600)

    # plot the accuracy
    plt.figure(figsize=(15,10))
    plt.plot(loss_train)
    plt.plot(loss_valid)
    plt.legend(['Training Accuracy', 'Validation Accuracy'], fontsize=FS)
    plt.xlabel('epoch', fontsize=FS)
    plt.ylabel('Accuracy', fontsize=FS)
    plt.tick_params(axis='both', labelsize=FS-5)
    plt.savefig('accCNNRNN.png', dpi=600)

    # plot the error

    plt.figure(figsize=(15,10))
    plt.plot(err_train)
    plt.plot(err_valid)
    plt.legend(['Training Error', 'Validation Error'], fontsize=FS)
    plt.xlabel('epoch', fontsize=FS)
    plt.ylabel('Error', fontsize=FS)
    plt.tick_params(axis='both', labelsize=FS-5)
    plt.savefig('errCNNRNN.png', dpi=600)

