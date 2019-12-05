import numpy as np
import pandas as pd
import os
import cv2
from sklearn.model_selection import train_test_split
from keras.applications.vgg19 import VGG19
from keras.optimizers import *
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
# from keras.preprocessing.image import load_img,img_to_array

#数値に変換
def trans_from_cup_to_int(name_value):
    name_array = ["A","B","C","D","E","F","G","H以上"]
    return name_array.index(name_value)

#データの読み込み
def load_data():
    print("start loading...")
    path = "data"
    name_list = [i for i in os.listdir(path) if i != '.DS_Store']
    pic_num = 0
    x_data = []
    y_label_data = []
    for name in name_list:
        label_value = trans_from_cup_to_int(name)
        pic_folder_path = path + "/" + name
        pic_list = [i for i in os.listdir(pic_folder_path) if i != '.DS_Store']
        for pic_name in pic_list:
            pic_path = pic_folder_path+"/"+pic_name
            img = cv2.imread(pic_path)
            x_data.append(img)
            y_label_data.append(label_value)
    x_data = np.array(x_data)
    y_label_data = np.array(y_label_data)
    print("loading has finished!")
    return x_data, y_label_data


def resize_picture(images):
    changed_images = []
    for img in images:
        img = cv2.resize(img, dsize=(100, 100))
        changed_images.append(img)
    changed_images = np.array(changed_images)
    return changed_images


def build_model():
    base_model=VGG19(weights='imagenet',include_top=False,
                 input_tensor=Input(shape=(100,100,3)))
    for layer in base_model.layers[:15]:
        layer.trainable=False
    model = Sequential()
    model.add(base_model)
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(1))
    model.compile(Adam(lr=1e-4,clipnorm=1), loss="mean_absolute_error")
    print("Build model!")
    return model


def fit_model(model, X_train, Y_train, X_val, Y_val):
    batch_size=16
    epochs = 20
    #とりあえずぼかし以外
    datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True
    )
    #ここから下はこれを参照https://lp-tech.net/articles/Y56uo
    early_stopping = EarlyStopping(monitor='val_loss', patience=1 , verbose=1)
    model.fit_generator(
        datagen.flow(X_train, Y_train, batch_size=batch_size),
        epochs = epochs,
        validation_data=(X_val,Y_val),
        callbacks=[early_stopping]
    )
    return model

def make_model():
    skf = StratifiedKFold(5, random_state = 0, shuffle = True)
    scores = []
    i = 0
    for k_fold, (tr_inds, val_inds) in enumerate(skf.split(X,Y)):
        X_train,Y_train = X[tr_inds],Y[tr_inds]
        X_val,Y_val = X[val_inds],Y[val_inds]
        model = build_model()
        model = fit_model(model,X_train,Y_train,X_val,Y_val)
        model.save('use_models/model'+str(i)+'.h5')
        i += 1
        del model

def make_dir()
    if not os.path.exists('use_models'):
        os.mkdir("use_models")

make_dir()
X, Y = load_data()
X = resize_picture(X)
make_model()
