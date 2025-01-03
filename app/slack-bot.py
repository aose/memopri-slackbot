import os
import time
import subprocess
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from PIL import Image, ImageDraw, ImageFont
import schedule
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_BOT_USER_ID = os.getenv("SLACK_BOT_USER_ID")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")


# 追跡する最後のメッセージのタイムスタンプ
last_timestamp = round(time.time(), 6)  # slackのtimestampは小数点以下6桁まで

def fetch_latest_messages():
    global last_timestamp
    print("Fetch...")
    try:
        # 最後に処理したメッセージ以降のメッセージを取得
        print("timestamp: ", last_timestamp)

        # Slackクライアントを初期化
        client = WebClient(token=SLACK_TOKEN)
        response = client.conversations_history(channel=CHANNEL_ID, oldest=last_timestamp, limit=3)
        
        messages = response.get("messages", [])
        for message in messages:
            if SLACK_BOT_USER_ID in message.get("text", ""):
                process_message(message["text"], message["ts"])
        
    except SlackApiError as e:
        print(f"Error fetching messages: {e}")

def process_message(text, timestamp):
    # メンション部分を除去し、メッセージ内容を取得
    content = text.replace("<@" + SLACK_BOT_USER_ID + ">", "").strip()
    print(f"Processing message: {content}")
    
    # メッセージを画像に変換
    create_image(content)
    
    # 最後に処理したメッセージのタイムスタンプを保存
    global last_timestamp
    last_timestamp = timestamp

    # プリンタを実行
    print("printing....")
    try:
        subprocess.run(["python3", "memopri.py", "input-image.png"])
    except Exception as e:
        print(f"Error printing: {e}")

    # 画像の削除
    delete_image("input-image.png")
    

def create_image(text):
    # フォントの設定
    fontpath = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    textsize = 20
    font = ImageFont.truetype(fontpath, textsize)
    
    # テキストのサイズを取得
    _, _, text_width, text_height = ImageDraw.Draw(Image.new("RGB", (1,1))).textbbox((0,0), text, font=font)

    # 画像の幅をテキストの幅に合わせて設定
    img_width = int(text_width) + 20  # 余白を追加
    img_height = 96  # 高さは固定
    
    # 画像を作成
    img = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(img)
    
    # テキストを画像に描画
    draw.text((10, (img_height - text_height) // 2), text, fill="black", font=font)
    
    # 画像を保存
    img.save("input-image.png")
    print("Image created: input-image.png")

def delete_image(image_path):
    try:
        os.remove(image_path)
        print(f"Deleted image: {image_path}")
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def main():
    # 定期的にメッセージをチェック
    schedule.every(20).seconds.do(fetch_latest_messages)
    
    print("App is running...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()