CASIO メモプリ（MEP-F10）をSlackBotからたたいて印刷するツール
----

# 必要なもの

- Slack
    - このへん見て `.env` に必要なトークン等を揃える
    - https://qiita.com/tatsuya1970/items/e45af6b4b2131979b940
- MEP-F10
    - IPアドレスで指定するので、事前にIPが固定されている必要あり
    - 無線LAN設定、IPアドレス固定にはMEP-F10のWindows用アプリが必要
- Docker実行環境

# 動き
起動の60秒前からのSlack投稿を印刷する

# 実行

`.env.sample` をもとに `.env` を作成する。

## 動作確認

```
docker run --rm -v $(pwd)/.env:/app/.env:ro ghcr.io/aose/memopri-slackbot:latest
```

## crontab登録
```
  * * * * * docker run --rm -v /path/to/memopri-slackbot/.env:/app/.env:ro ghcr.io/aose/memopri-slackbot:latest
```


# 参考
Dockerで動かすので接続は固定IPにした
https://gist.github.com/marcan/6ea02bc0daf8dcb4acc74024a4df21b8