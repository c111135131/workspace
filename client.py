import re
from linebot.models import *
from database import check_clientId, save_user_to_database
from ai_reply import handle_customer_service
import os
from dotenv import load_dotenv
from utils import validate_phone_number, request_name_and_phone,show_menu, ask_quantity,confirm_order

load_dotenv()

user_data = {}
orders = {}

def handle_client_message(event, line_bot_api):
    user_message = event.message.text.strip()
    user_id = event.source.user_id

    if check_clientId(user_id):
        if user_id in orders and "quantity" not in orders[user_id]:
            if user_message.isdigit():
                orders[user_id]["quantity"] = int(user_message)
                confirm_order(event, line_bot_api, user_id,orders)
                print(orders)
            else:
                line_bot_api.reply_message(event.reply_token, TextMessage(text="請輸入正確的數字作為數量。"))
        elif "線上訂購" in user_message:
            show_menu(event, line_bot_api)
        elif user_message in ["草莓奶油蛋糕", "巧克力慕斯", "芒果椰漿布丁", "檸檬塔"]:
            ask_quantity(event, line_bot_api, user_id, user_message, orders)
        else:
            reply = handle_customer_service(user_message)
            line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))
    else:
        if user_id not in user_data:
            request_name_and_phone(event, line_bot_api, user_id, user_data)
        else:
            if user_data[user_id]["waiting_for"] == "name":
                user_data[user_id]["name"] = user_message
                user_data[user_id]["waiting_for"] = "phone"
                line_bot_api.reply_message(event.reply_token, TextMessage(text="請輸入您的電話號碼："))
            elif user_data[user_id]["waiting_for"] == "phone":
                phone = user_message
                if validate_phone_number(phone):
                    name = user_data[user_id]["name"]
                    save_user_to_database(user_id, name, phone)
                    del user_data[user_id]
                    line_bot_api.reply_message(event.reply_token, TextMessage(text=f"註冊完成！歡迎光臨！"))
                else:
                    line_bot_api.reply_message(event.reply_token, TextMessage(text="電話格式不正確，請重新輸入。"))
