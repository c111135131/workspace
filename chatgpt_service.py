import openai

class ChatGPTService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_response(self, user_message):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一個專業的甜點訂購助手，友善、專業地幫助顧客訂購甜點。"},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"對不起，無法處理您的請求：{str(e)}"