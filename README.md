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


# 実行

`.env.sample` をもとに `.env` を作成する。

```
docker build -t memopri-slack .
docker run --restart always -d --name memopri-slack -v $(pwd)/.env:/app/.env:ro memopri-slack
```

# 参考
Dockerで動かすので接続は固定IPにした
https://gist.github.com/marcan/6ea02bc0daf8dcb4acc74024a4df21b8