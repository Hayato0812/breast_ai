import json, config
from requests_oauthlib import OAuth1Session
from urllib import request
import numpy as np
from PIL import Image
import schedule
import datetime

dt_now = datetime.datetime.now()


CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

search_url = "https://api.twitter.com/1.1/search/tweets.json"
create_url = "https://api.twitter.com/1.1/statuses/update.json"

text = "今の時刻は"+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+" だよ"

params = {"status": text}
twitter = OAuth1Session(CK, CS, AT, ATS)
twitter.post(create_url, params = params)
