from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def handle_ai_reply():

    user_message = "hello?"

    endpoint = os.getenv('OPENAI_ENTPOINT')
    key = os.getenv('OPENAI_API_KEY')  # Your API key

    print(endpoint, key)
    model_name = "gpt-35-turbo"  # Your model name

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_version="2024-08-01-preview",
        api_key=key
    )

    completion = client.chat.completions.create(
        model=model_name,
        # seed=42,
        # temperature = 1.0,
        # max_tokens =150, 
        messages=[
             {
		        "role": "assistant",
		        "content": "你是一個甜點店的老闆；先確認客人訂單，禮貌回覆訊息；"
	        },

            {
                "role": "user",
                "content": user_message,  # Your question can go here
            },
        ],
    )

    reply = completion.choices[0].message.content
    print(reply)

handle_ai_reply()



