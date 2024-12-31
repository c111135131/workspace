import re
from linebot.models import TextMessage
from database import check_clientId, save_user_to_database
from ai_reply import handle_customer_service

user_data = {}

# 檢查電話格式
def validate_phone_number(phone_number):
    pattern = re.compile(r"^\d{10}$")
    return pattern.match(phone_number) is not None

# 顯示文字訊息，提醒用戶輸入名字或電話
def request_name_and_phone(event, line_bot_api, user_id):
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text="請先輸入'您的名字'以完成註冊喔")
    )
    # 初始化用戶資料，並設置正在等待名字輸入
    user_data[user_id] = {"name": None, "phone": None, "waiting_for": "name"}

def handle_client_message(event, line_bot_api):
    user_message = event.message.text.strip()
    print(type(user_message))
    user_id = event.source.user_id
    print(type(user_id))
    print(user_data)
    # 檢查用戶是否已註冊
    if check_clientId(user_id):
        # 已註冊用戶處理
        if "下訂單" in user_message:
            reply = "請提供您要下訂單的商品資訊，我們會盡快處理！"
        else:
            reply = handle_customer_service(user_message)
    else:
        # 未註冊用戶，處理名字和電話的輸入
        if user_id not in user_data:
            # 顯示提示文字，請用戶輸入名字
            request_name_and_phone(event, line_bot_api, user_id)
            return
        else:
            # 根據用戶的輸入處理名字或電話
            if user_data[user_id]["waiting_for"] == "name":

                user_data[user_id]["name"] = user_message
                reply = f"名字已記錄為：{user_message}，請繼續正確輸入輸入'您的電話'"
                user_data[user_id]["waiting_for"] = "phone"  # 更新為等待輸入電話
                line_bot_api.reply_message(event.reply_token, TextMessage(text="請輸入您的電話號碼"))

            elif user_data[user_id]["waiting_for"] == "phone":
                phone = user_message
                if validate_phone_number(phone):
                    
                    user_data[user_id]["phone"] = phone
                    name = user_data[user_id]["name"]
                    save_user_to_database(user_id, name, phone)
                    
                    reply = f"註冊完成！\n姓名：{name}\n電話：{phone}"
                    del user_data[user_id]  # 清除暫存資料
                 
                else:
                    reply = "電話格式不正確，請重新輸入 10 位數字電話號碼。"
            else:
                reply = "請按照提示輸入您的名字或電話。"

    # 發送回應給用戶
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))
