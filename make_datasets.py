import numpy as np
import pandas as pd
import os
import cv2
from sklearn.model_selection import train_test_split
from keras.applications.vgg19 import VGG19
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.callbacks import EarlyStopping, ModelCheckpoint
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

#データの大きさ揃える、とりあえず150*150で様子見
def resize_picture(images):
    changed_images = []
    for img in images:
        img = cv2.resize(img, dsize=(200, 200))
        changed_images.append(img)
    changed_images = np.array(changed_images)
    return changed_images

#データの切り取りによるかさまし、いらないかも
def make_more_data(images):
    trans_images = []
    for image in images:
        cut_img = img[img.shape[0]//6:img.shape[0]*5//6,img.shape[1]//6:img.shape[1]*5//6]
        trans_images.append(cut_img)
    images.extend(trans_images)
    return images

def build_model():
    base_model=VGG19(weights='imagenet',include_top=False,
                 input_tensor=Input(shape=(200,200,3)))
    x=base_model.output
    x=GlobalAveragePooling2D()(x)
    x=Dense(1024,activation='relu')(x)
    prediction=Dense(1)(x)
    model=Model(inputs=base_model.input,outputs=prediction)

    for layer in base_model.layers[:15]:
        layer.trainable=False

    model.compile(Adam(lr=1e-3), loss="mean_squared_error")
    print("Build model!")
    return model


def fit_model(model):
    samples_per_epoch = 20
    batch_size=32
    epochs = 10
    #とりあえずぼかし以外
    datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True
    )
    #ここから下はこれを参照https://lp-tech.net/articles/Y56uo
    early_stopping = EarlyStopping(monitor='val_loss', patience=10 , verbose=1)
#     checkpointer = ModelCheckpoint(
#         model_weights,
#         monitor='val_loss',
#         verbose=1,
#         save_best_only=True
#         )
    print(Y_train.shape)
    history = model.fit_generator(
        datagen.flow(X_train, Y_train, batch_size=20),
        epochs = epochs,
        validation_data=(X_val,Y_val),
        callbacks=[early_stopping]
    )
    return model


x_data, y_label_data = load_data()
x_data = resize_picture(x_data)
model = build_model()
random_seed = 0
X_train, X_val, Y_train, Y_val = train_test_split(x_data, y_label_data, random_state=random_seed)
model = fit_model(model)
