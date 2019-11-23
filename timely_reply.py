# https://gukoulog.com/2018/09/22/python-2/

from requests_oauthlib import OAuth1Session
import json, config
#４つのキーをセット
CK = CONSUMER_KEY
CS = CONSUMER_SECRET
AT = ACCESS_TOKEN
ATS =　ACCESS_TOKEN_SECRET

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update.json"

# パラメータ設定
params = {"status": "PythonでTwitter APIテスト中です"}

# OAuth
twitter = OAuth1Session(CK, CS, AT, ATS)
req = twitter.post(url, params = params)

# レスポンスを確認
if req.status_code == 200:
    print ("Done")
else:
    print ("Error: %d" % req.status_code)
