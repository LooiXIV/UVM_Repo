Code to reformat preprocessed data from the Brats2017 Kaggle competition and to train a CNN-LSTM model that performs semantic brain tumor segemtation.

The Image_Preprocess.ipynb file is a jupyter notebook that further processes brain MRI images taken from the 2017 Brats Kaggle competition. Here, the data is taken from the .nii MRI image files and converted to numpy arrays, reshaped into 4D arrays, and stored as a numpy type file in binary. These are the files that the CNN-LSTM is trained on.

Each brain has its own training set and a truth mask. The truth masks should have the same number of dimensions as the training images. There is a difference between the two image types, the last dimension. The last dimension for the training set denotes the number of channels in an image. In this case each channel is a modality with four modailities in total (a seperate type of MRI image). In the test set there is only a single channel. 

Shapes for the training images should be (155, 240, 240, 4). Here the first dimension refer to layers in brain image, the next two dimesions correspond to x and y rows of a brain image, and the last dimensions refers to each channel. In the test set the Shapes should be (155, 240, 240, 1). Here all but the last dimensions represent the same parts of the brain image. The last dimensions in the test images are the truth masks which represent tumors as marked and defined by a professional human classifier. 

The CNN_RNN_Brats17.py file holds the model, the code to train the model, and the code to plot the learning curves. Simply call $ python CNN_RNN_Brats17.py. 
