from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from linebot.models import TextMessage
from database import get_unprocessed_orders, get_monthly_sales_report()

def handle_client_message(event, line_bot_api):
    user_message = event.message.text.lower()

    if "下訂單" in user_message:
        orders = get_unprocessed_orders()
        if orders:
            reply = "\n".join([f"訂單ID: {o['id']}, 商品: {o['item_name']}, 數量: {o['quantity']}" for o in orders])
        else:
            reply = "目前沒有未處理的訂單。"
    
    else:


    # 發送回應給管理員
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=reply)
    )
