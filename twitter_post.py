from twitter import Twitter, OAuth
import json, config

access_token = config.CONSUMER_KEY
access_token_secret = config.CONSUMER_SECRET
api_key = config.ACCESS_TOKEN
api_secret = config.ACCESS_TOKEN_SECRET

t = Twitter(auth = OAuth(access_token, access_token_secret, api_key, api_secret))

text = 'Pythonを使ってつぶやいてみました。'
statusUpdate = t.statuses.update(status=text)

# 生の投稿データの出力
print(statusUpdate)

# 要素を絞った投稿データの出力
print(statusUpdate['user']['screen_name'])
print(statusUpdate['user']['name'])
print(statusUpdate['text'])
