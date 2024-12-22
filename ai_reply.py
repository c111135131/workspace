from linebot.models import TextSendMessage

def handle_ai_reply(event, line_bot_api):
    text = event.message.text.lower()
    if "營業時間" in text:
        reply = "我們的營業時間是每天早上9點到晚上9點。"
    elif "配送時間" in text:
        reply = "配送時間約為1-2天，請耐心等候！"
    elif "聯絡方式" in text:
        reply = "您可以透過客服專線 0800-123-456 聯繫我們。"
    else:
        reply = "抱歉，我不太明白您的問題，可以稍微描述清楚一點嗎？"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))