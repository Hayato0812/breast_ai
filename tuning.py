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
from statistics import mean
import optuna
from sklearn.model_selection import KFold
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
    y_label_data = np.array(y_label_data).astype('int8')
    print("loading has finished!")
    return x_data, y_label_data

#データの大きさ揃える
def resize_picture(images):
    changed_images = []
    for img in images:
        img = cv2.resize(img, dsize=(100, 100))
        changed_images.append(img)
    changed_images = np.array(changed_images).astype('int8')
    return changed_images

#データの切り取りによるかさまし、いらないかも
def make_more_data(images):
    trans_images = []
    for image in images:
        cut_img = img[img.shape[0]//6:img.shape[0]*5//6,img.shape[1]//6:img.shape[1]*5//6]
        trans_images.append(cut_img)
    images.extend(trans_images)
    return images

def build_model(structure_params):
    base_model=VGG19(weights='imagenet',include_top=False,
                 input_tensor=Input(shape=(100,100,3)))
    for layer in base_model.layers[:15]:
        layer.trainable=False
    model = Sequential()
    model.add(base_model)
    model.add(Flatten())
    if structure_params["num_layers"] >= 1:
        model.add(Dense(structure_params["first_param_num"]))
        model.add(Activation('relu'))
        model.add(Dropout(structure_params["first_dropout_rate"]))
        if structure_params["num_layers"] >= 2:
            model.add(Dense(structure_params["second_param_num"]))
            model.add(Activation('relu'))
            model.add(Dropout(structure_params["second_dropout_rate"]))
            if structure_params["num_layers"] >= 3:
                model.add(Dense(structure_params["third_param_num"]))
                model.add(Activation('relu'))
    model.add(Dense(1))
    model.compile(optimizer=Adam(lr=0.001), loss="mean_absolute_error")
    return model

def use_model(model, X_train, Y_train, X_val, Y_val):
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
    early_stopping = EarlyStopping(monitor='val_loss', patience=3 , verbose=0)
    history = model.fit_generator(
        datagen.flow(X_train, Y_train, batch_size=batch_size),
        epochs = epochs,
        validation_data=(X_val,Y_val),
        callbacks=[early_stopping]
    )
    return history.history["val_loss"][-1]

def objective(trial):
    # optimizer = trial.suggest_categorical("optimizer", ["sgd", "adam", "rmsprop"])
    num_layers = trial.suggest_int('num_layers', 0, 3)
    first_dropout_rate = trial.suggest_uniform('first_dropout_rate', 0.0, 0.5)
    second_dropout_rate = trial.suggest_uniform('second_dropout_rate', 0.0, 0.5)
    first_param_num =  trial.suggest_categorical("first_param_num", [256,512])
    second_param_num = trial.suggest_categorical("second_param_num", [32,64,128])
    third_param_num = trial.suggest_categorical("third_param_num", [16,32,64])
    structure_params = {
        # "optimizer": optimizer,
        "num_layers": num_layers,
        "first_dropout_rate": first_dropout_rate,
        "second_dropout_rate": second_dropout_rate,
        "first_param_num": first_param_num,
        "second_param_num": second_param_num,
        "third_param_num": third_param_num
    }

    kfold = KFold(5, random_state = 0, shuffle = True)
    scores = []
    print(structure_params)
    for k_fold, (tr_inds, val_inds) in enumerate(kfold.split(X)):
        X_train,Y_train = X[tr_inds],Y[tr_inds]
        X_val,Y_val = X[val_inds],Y[val_inds]
        model = build_model(structure_params)
        score = use_model(model,X_train,Y_train,X_val,Y_val)
        scores.append(score)
    print("score→ "+str(mean(scores)))
    params_and_scores.append([structure_params,mean(scores)])
    return mean(scores)


X, Y = load_data()
X = resize_picture(X)
params_and_scores = []
study = optuna.create_study()
study.optimize(objective, n_trials=50)
print("params_{}".format(study.best_params))
print("value_{}".format(study.best_value))
print(params_and_scores)
