from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from client import handle_client_message
from admin import handle_admin_command
from database import init_database  # 匯入資料庫初始化
from dotenv import load_dotenv
import os
from utils import handle_postback
from client import orders
import re

app = Flask(__name__)

load_dotenv()

# 設定 LINE Bot
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 初始化資料庫
init_database()

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    print(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    # print(f'您的管理者ID為:{userId}')
    ADMIN_ID = os.getenv('ADMIN_ID')

    if re.match(userId,ADMIN_ID):  # 管理員功能
        handle_admin_command(event, line_bot_api)
        
    else:  # 使用者訊息
        handle_client_message(event, line_bot_api)

@handler.add(PostbackEvent)
def handle_postback_event(event):
    handle_postback(event, line_bot_api,orders)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


