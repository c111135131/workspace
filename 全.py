# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('馬哥甜點店')
# 必須放上自己的Channel Secret
handler = WebhookHandler('你自己的secret')

line_bot_api.push_message('你自己的ID', TextSendMessage(text='甜點優惠活動開始囉！'))

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
    message = text=event.message.text
    if re.match('甜點優惠', message):
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/xyz123.jpg',
            alt_text='甜點優惠活動',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://dessertshop.com/promotion',
                    area=ImagemapArea(
                        x=0, y=0, width=520, height=1040
                    )
                ),
                MessageImagemapAction(
                    text='立即參加優惠活動！',
                    area=ImagemapArea(
                        x=520, y=0, width=520, height=1040
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    elif re.match('季節活動', message):
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/abc456.jpg',
            alt_text='季節活動資訊',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://dessertshop.com/seasonal-event',
                    area=ImagemapArea(
                        x=0, y=0, width=520, height=1040
                    )
                ),
                MessageImagemapAction(
                    text='立即了解活動詳情！',
                    area=ImagemapArea(
                        x=520, y=0, width=520, height=1040
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    elif re.match('甜點選單',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='甜點選單',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
            title='甜點選單',
            text='請選擇以下選項',
            actions=[
                URIAction(
                    label='甜點訂購',
                    uri='https://dessertshop.com/order'
                ),
                URIAction(
                    label='查看甜點菜單',
                    uri='https://dessertshop.com/menu'
                ),
                URIAction(
                    label='訂購資訊查詢',
                    uri='https://dessertshop.com/info'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
