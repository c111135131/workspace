from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message =event.message.text
    server = os.getenv('SERVER_URL')

    #從這裡開始改!!!!!
    if re.match('新品推薦', message):
        imagemap_message = ImagemapSendMessage(
            base_url=f'{server}/image/你的圖片.jpg',  # 图片的基本 URL，指向新品推薦的图片
            alt_text='新品推薦',  # 当图片无法显示时的替代文本
            base_size=BaseSize(height=1040, width=1040), 
            actions=[
                MessageImagemapAction(
                    text='新品推薦介紹',  # 点击后发送的消息文本
                    area=ImagemapArea(
                        x=520, y=0, width=1040, height=1040 
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)

    #以此類推改下來
    elif re.match('熱門甜點', message):
        imagemap_message = ImagemapSendMessage(
            base_url=f'{server}/image/你的圖片.jpg',  # 图片的基本 URL，指向新品推薦的图片
            alt_text='新品推薦',  # 当图片无法显示时的替代文本
            base_size=BaseSize(height=1040, width=1040), 
            actions=[
                MessageImagemapAction(
                    text='新品推薦介紹',  # 点击后发送的消息文本
                    area=ImagemapArea(
                        x=520, y=0, width=1040, height=1040 
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)

    elif re.match('菜單資訊', message):
        imagemap_message = ImagemapSendMessage(
            base_url=f'{server}/image/你的圖片.jpg',  # 图片的基本 URL，指向新品推薦的图片
            alt_text='新品推薦',  # 当图片无法显示时的替代文本
            base_size=BaseSize(height=1040, width=1040), 
            actions=[
                MessageImagemapAction(
                    text='新品推薦介紹',  # 点击后发送的消息文本
                    area=ImagemapArea(
                        x=520, y=0, width=1040, height=1040 
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
