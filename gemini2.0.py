import os
import google.generativeai as generativeai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# 設定 Google Generative AI 的 API 金鑰
generativeai.configure(api_key=os.getenv('API_KEY'))

def generate_text(text):

    # 使用 Google Generative AI 生成文字
    res = generativeai.GenerativeModel('gemini-2.0-flash-exp').generate_content(text)
    
    # 返回生成的文字
    return res.text

if __name__ == "__main__":

    text = '你好嗎?' #prompt
    generated_text = generate_text(text)
    print(f"Generated text: {generated_text}")