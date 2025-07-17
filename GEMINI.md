# GEMINI CLI コンテキスト: memopri-slackbot

このファイルは、`memopri-slackbot` リポジトリに関する主要な情報と、今後のCLI操作で役立つコンテキストをまとめたものです。

## 1. プロジェクト概要

CASIO メモプリ（MEP-F10）をSlackBotから操作し、Slackの投稿内容を印刷するためのツールです。Docker環境での実行を前提としています。

## 2. 主要ファイルと役割

*   **`README.md`**:
    *   プロジェクトの概要、必要なもの、動作、実行方法（Docker、crontab登録例）が記載されています。
*   **`app/slack-bot.py`**:
    *   Slackとの連携（`slack_sdk` を使用）。
    *   指定されたチャンネルからメッセージを取得し、ボットへのメンションがあるメッセージを抽出。
    *   抽出したメッセージ内容を `PIL` (Pillow) を使用して画像に変換（フォント: `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`）。
    *   生成した画像を `memopri.py` に渡して印刷処理を依頼。
    *   環境変数 (`SLACK_BOT_TOKEN`, `SLACK_BOT_USER_ID`, `SLACK_CHANNEL_ID`) を使用。
    *   定期実行を想定しており、前回のタイムスタンプ以降のメッセージのみを処理します。
*   **`app/memopri.py`**:
    *   MEP-F10 プリンターとの直接通信（ソケット通信、ポート16402）。
    *   `PIL` (Pillow) を使用して、入力画像をプリンターが認識できる形式（1ビット深度、ディザリング、最大幅96px）に変換。
    *   プリンター固有のコマンドを送信して印刷を実行。
    *   環境変数 (`MEMOPRI_IP_ADDRESS`) を使用。
*   **`.env.sample`**:
    *   必要な環境変数のテンプレート。`.env` ファイルを作成する際の参考にします。
*   **`Dockerfile`**:
    *   アプリケーションをDockerコンテナとしてビルドするための定義ファイル。

## 3. コア機能とワークフロー

1.  `slack-bot.py` がSlackチャンネルから新しいメッセージを定期的に監視。
2.  ボットへのメンションが含まれるメッセージを抽出。
3.  メッセージ内容を画像ファイル (`input-image.png`) として生成。
4.  `memopri.py` を呼び出し、生成された画像をメモプリで印刷。
5.  印刷後、一時画像ファイルを削除。

## 4. 使用技術・ライブラリ

*   **言語**: Python
*   **Slack連携**: `slack_sdk`
*   **画像処理**: `Pillow` (PIL)
*   **環境変数管理**: `python-dotenv`
*   **実行環境**: Docker

## 5. 想定される運用と制約

*   **メモプリのIPアドレス固定**: MEP-F10プリンターのIPアドレスは固定されており、環境変数 `MEMOPRI_IP_ADDRESS` で指定されます。
*   **定期実行**: `crontab` などによる定期的な実行が想定されています（例: 1分ごとにSlackをチェック）。
*   **フォント**: 画像生成には `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` が使用されます。
*   **画像幅の制約**: メモプリの印刷幅の制約により、生成される画像の幅は96ピクセル以下である必要があります。

---
この情報が今後の作業に役立つことを願っています。
