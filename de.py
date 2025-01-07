# -*- coding: utf-8 -*-
"""
Line Bot聊天機器人 - 選單功能 (ConfirmTemplate)
Created by Ivan
版權屬於「行銷搬進大程式」，如有疑問，聯絡 ivanyang0606@gmail.com
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
import os

app = Flask(__name__)

# 設定 Line Bot 的 Channel Access Token 和 Secret
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', '你的token')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET', '你的secret')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 初始推送訊息給指定的用戶
USER_ID = '你的ID'
line_bot_api.push_message(USER_ID, TextSendMessage(text='你可以開始了'))

# 監聽來自 /callback 的 POST 請求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理收到的訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    received_text = event.message.text

    if re.match('告訴我秘密', received_text):
        confirm_template = TemplateSendMessage(
            alt_text='問問題',
            template=ConfirmTemplate(
                text='你喜歡這堂課嗎？',
                actions=[
                    PostbackAction(
                        label='喜歡',
                        display_text='超喜歡',
                        data='action=喜歡'
                    ),
                    MessageAction(
                        label='愛',
                        text='愛愛❤'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=received_text))

# 主程式入口
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
