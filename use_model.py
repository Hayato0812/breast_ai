from keras.models import load_model
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
from statistics import mean
import cv2

def resize_picture(image):
    image = cv2.resize(image, dsize=(100, 100)).astype('int8')
    image = np.reshape(image, (1, 100, 100, 3))
    return image

def load_models():
    models = []
    for i in range(5):
        models.append(load_model('use_models/model'+str(i)+'.h5'))
    return models

def predict(models,image):
    preds = []
    for model in models:
        pred = model.predict(image, batch_size=1, verbose=0)[0][0]
        preds.append(pred)
    return mean(preds)

def comment_content(pred):
    if pred<=1:
        content = "真っ平らのAカップじゃ"
    elif pred<=2:
        content = "Bカップか、平均くらいだのう"
    elif pred<=3:
        content = "Cカップ、ちょうどいいサイズじゃな"
    elif pred<=4:
        content = "Dカップとはかなり大きめの部類じゃな"
    elif pred<=5:
        content = "Eカップとはとても大きいのう、、、"
    elif pred<=6:
        content = "Fカップ！とても大きい胸じゃのう、、、、"
    elif pred<=7:
        content = "Gカップじゃと、、、こんな大きいのみたことないぞい、、、"
    else:
        content = "Hカップ以上、、、これは幻覚か、天国が広がってるぞい、、、"
    return content

def use_this_file(models, file_name):
    # filename = "test_picture/F馬場ふみか.jpg"
    image = cv2.imread(file_name)
    image = resize_picture(image)
    pred = predict(models,image)
    print(file_name)
    print(pred)

# if __name__ == '__main__':
#     file_paths = ["test_picture/F馬場ふみか.jpg","test_picture/Aカップ清水富美加.jpg","test_picture/Dカップ.jpg"]
#     models = load_models()
#     for file_path in file_paths:
#         use_this_file(models,file_path)
