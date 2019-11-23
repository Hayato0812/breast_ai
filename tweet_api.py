import json, config
from requests_oauthlib import OAuth1Session
# from urllib import request
import numpy as np
from PIL import Image
import schedule



CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

search_url = "https://api.twitter.com/1.1/search/tweets.json"
create_url = "https://api.twitter.com/1.1/statuses/update.json"

print("何を調べますか?")
keyword = '@breast_pred_ai'
print('----------------------------------------------------')


params = {'q' : keyword, 'count' : 5}

req = twitter.get(search_url, params = params)

if req.status_code == 200:
    tweet_ids = []
    search_result = json.loads(req.text)
    i = 0
    for tweet in search_result['statuses']:
        screen_name = tweet["user"]['screen_name']
        if list(tweet.keys()).count('extended_entities')==1:
            img = tweet['extended_entities']["media"][0]["media_url"]
            img = request.urlopen(img).read()
            img = np.array(Image.frombuffer('RGB', (100,100), img))
            content = str(img.shape)
        else:
            print(tweet["text"])
            content = "写真が入ってないか２枚以上入ってるよ"
        print('----------------------------------------------------')
        params = {"status": "@"+screen_name+ " "+content}
        twitter.post(create_url, params = params)
else:
    print("ERROR: %d" % req.status_code)

schedule.every(10).minutes.do(job)
