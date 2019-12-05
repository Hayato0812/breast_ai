import json, config
from requests_oauthlib import OAuth1Session
from urllib import request
import numpy as np
from PIL import Image
import schedule
import datetime
from datetime import timedelta
from use_model import resize_picture, load_models, predict, comment_content
import time
import cv2
import io
from matplotlib import pylab as plt
import tweepy


dt_past = datetime.datetime.now() - timedelta(minutes=10)



CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth)

search_url = "https://api.twitter.com/1.1/search/tweets.json"
create_url = "https://api.twitter.com/1.1/statuses/update.json"

dt_past_date = str(dt_past).split(" ")[0]
dt_past_hm = dt_past.strftime("%H:%M")
keyword =  "@breast_pred_ai since:" + dt_past_date + "_"+ str(dt_past_hm)+"_JST"

params = {'q' : keyword, 'count' : 50}

req = twitter.get(search_url, params = params)

if req.status_code == 200:
    models = load_models()
    tweet_ids = []
    search_result = json.loads(req.text)
    for tweet in search_result['statuses']:
        print(tweet)
        tweet_id = tweet['id']
        screen_name = tweet["user"]['screen_name']
        try:
            api.create_favorite(tweet_id)
            if list(tweet.keys()).count('extended_entities')==1:
                img = tweet['extended_entities']["media"][0]["media_url"]
                img = request.urlopen(img).read()
                img = np.asarray(bytearray(img),dtype="uint8")
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                img = resize_picture(img)
                pred = predict(models,img)
                content = comment_content(pred)
                # content += "という結果が出ました"+str(pred)
            else:
                content = "写真が入ってないぞい"
            params = {"status": "@"+screen_name+ " "+content,'in_reply_to_status_id': tweet_id}
            # params = {"status": "@"+screen_name+ " "+content}
            twitter = OAuth1Session(CK, CS, AT, ATS)
            twitter.post(create_url, params = params)
        except:
            print("もういいねされてます")
            continue
else:
    print("ERROR: %d" % req.status_code)
