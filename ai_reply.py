from openai import ChatCompletion
import os
from linebot.models import TextMessage  

openai_api_key = os.getenv("OPENAI_API_KEY")

# AI 回覆處理器
def handle_ai_reply(event, line_bot_api):
    user_message = event.message.text

    try:
        # 使用 OpenAI API 生成回應
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            api_key=openai_api_key
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"AI 回覆失敗: {str(e)}"

    # 發送回應給使用者
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=reply) 
    )
