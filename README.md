# breast_ai

胸の大きさ（カップ数）を推定します。
### config.py→twitterアカウントのトークンとか、各自取得してね

### make_models.py→tuning.pyのパラメータを利用して作る、これやらないとmodel_timely_reply.pyが動かないよ

### model_timely_reply.py→これをlocalで定期実行にすることでサービスが動くよ

### requirements.txt→もともとherokuを使うつもりだったからあるけどいらないよ

### tuning.py→modelの層の数とかのtuningだよ、GCP使わないと鬼のように時間かかるし使っても物によってはtuningの途中で落ちるよ

### tweet_api_regulary.py→テストで定期実行するやつ

### use_model.py→この中身をmodel_timely_reply.pyから呼び出してるよ


## そのほか
・make_models.pyを動かすことでuse_modelsフォルダの作成と5つのmodelが入るようになってるが、容量が重いのでgitには上げてない
・もともとherokuを使って定期実行するつもりでheroku_env入ってるけどお金かかるようになったらしく、結局herokuは使ってない
