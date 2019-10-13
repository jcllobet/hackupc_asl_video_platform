import cv2
import requests
import argparse
# Imports for Deep Learning
from keras.layers import Dense, Dropout
from keras.models import Sequential,Model
from keras.preprocessing.image import ImageDataGenerator
from keras import regularizers
from keras.losses import categorical_crossentropy
from keras.applications.inception_v3 import InceptionV3
# ensure consistency across runs
from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(2)

# Imports to view data
# import cv2
from glob import glob
from matplotlib import pyplot as plt
from numpy import floor
import random


parser = argparse.ArgumentParser(description='Add video url and name to fetch and analyze')
parser.add_argument('--url', metavar='u', type=str, nargs='+', help='video url')
parser.add_argument('--name', type='str', help='filename')
parser.add_argument('--output', type='str', help='output directory')
args = parser.parse_args()


labels = list('abcdefghijklmnopqrstuvwxyz ')
labels.append('delete')
labels.append('nothing')

target_size = (224, 224)
target_dims = (224, 224, 3) # add channel for RGB
n_classes = 29
val_frac = 0.1
batch_size = 64

data_augmentor = ImageDataGenerator(samplewise_center=True, 
                                    samplewise_std_normalization=True, 
                                    validation_split=val_frac)


def load_image(imframe):
    img = np.asarray(cv2.resize(imframe, target_size))
    mean, std = img.mean(), img.std()
    img = (img - mean) / std
    return img



def downloadfile(name,url):
    name='./uploads/videos/'+name+".mp4"
    r=requests.get(url)
    print("****Connected****")
    f=open(name,'wb')
    print("Donloading.....")
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print("Done")
    f.close()



base_model = InceptionV3(include_top = False, weights=None, input_shape = target_dims, pooling='max')
# f = Flatten()(base_model.output)
dr = Dropout(0.5)(base_model.output)
d1 = Dense(512, activation = 'relu', kernel_regularizer = regularizers.l1(0.001))(dr)
d2 = Dense(n_classes, activation = 'softmax')(d1)
vggmodel = Model(base_model.input, d2)


vggmodel.load_weights('vggmodel.h5')
vggmodel.compile(optimizer = 'adam', loss = categorical_crossentropy, metrics = ["accuracy"])

target_size = (224,224)


link = args['url']  ##"https://media.videoask.it/transcoded/aaqn3pjhxx6oywnk.mp4" ##change to argparse
name = args['name']

downloadfile(name, link)


font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,50)
fontScale              = 2
fontColor              = (0,0,0)
lineType               = 2

cap = cv2.VideoCapture('./uploads/videos/'+name+".mp4")   ### change to argparse
# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

# Read until video is completed
frame_i=0
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame1 = cap.read()
    frame_i+=1
    if ret == True:
        ### detect hand first then do prediction
        
        frame = frame1[120:-150,400:-350]
        ### sign prediction
        yhat = np.argmax(vggmodel.predict(np.asarray([load_image(frame)])))

        # Display the resulting frame
        cv2.save('./uploads/'+args['output']+'/'+ labels[yhat].upper() +'-frame_'+str(frame_i),frame)
        
 
  # Break the loop
    else: 
        break

# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()