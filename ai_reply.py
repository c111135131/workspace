from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def handle_customer_service(user_message):

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
        seed=42,
        temperature = 0.7,
        max_tokens =100, 
        messages=[
             {
		        "role": "system",
		        "content": """
                # 甜點店購買須知

                1. **營業時間**  
                本店營業時間為 **每日 10:00 - 20:00**，如有特殊營業日或公休，將提前公告於官網與社群平台。

                2. **預訂訂單**  
                - 請於取貨日期前至少 **2 天**完成預訂。  
                - 預訂可於現場、Line聊天室或電話完成。

                3. **取貨方式**  
                - 店內取貨：請於營業時間內憑電話末三碼及姓名領取或訂單QRcode。  

                4. **付款方式**  
                - 本店接受現金、信用卡、行動支付（如 Apple Pay、Google Pay）以及銀行轉帳。
                - 請於本店付款
                
                5. **取消與更改**  
                - 訂單取消請於取貨前 **24 小時**通知，否則訂金不予退還。  
                - 訂單更改需提前聯繫，視可用性而定。

                6. **產品保鮮**  
                - 所有甜點均採用新鮮食材製作，請於購買當日或標示的保存期限內享用。  
                - 冷藏保存建議溫度為 **0-4°C**，冷凍甜點請存放於 **-18°C**。

                7. **過敏資訊**  
                - 本店甜點可能含有堅果、乳製品、蛋類或麩質，對食物過敏者請務必提前告知。

                8. **特製訂單**  
                - 若需定製特殊甜點（如生日蛋糕、婚禮甜品），請於 **7 天前**聯繫我們，以便協助設計和製作。
                - 點選下訂單->客製化商品->描述您想要的產品樣式->將生成蛋糕圖片

                9. **退換貨政策**  
                - 甜點屬於易腐商品，一經售出，除產品有明顯品質問題外，恕不接受退換。  
                - 如有問題，請於取貨後 **2 小時內**聯繫我們，並提供憑證。

                依照客人使用的語言回覆
                """
	        },

            {
                "role": "user",
                "content": user_message,  # Your question can go here
            },
        ],
    )

    return completion.choices[0].message.content
