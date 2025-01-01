from linebot.models import *
import os
from utils import handle_order_completion,show_unprocessed_orders,show_sales_report,prompt_for_order_id,reply_unknown_command

# 用來存儲管理員的會話狀態
user_sessions = {}

# 管理員指令處理器
def handle_admin_command(event, line_bot_api):
    user_message = event.message.text.lower()
    user_id = event.source.user_id  # 確保每個管理員的指令對應到正確的會話
    server = os.getenv('SERVER_URL')

    # 管理員會話狀態管理
    if user_id in user_sessions:
        session_state = user_sessions[user_id]
    else:
        session_state = None

    if session_state == "waiting_for_order_id":
        handle_order_completion(user_message, user_id, event, line_bot_api,user_sessions)
    elif "未處理訂單" in user_message:
        show_unprocessed_orders(event, line_bot_api, server)
    elif "銷售報表" in user_message:
        show_sales_report(event, line_bot_api, server)
    elif "發送完成訂單通知" in user_message:
        prompt_for_order_id(event, line_bot_api,user_sessions)
    else:
        reply_unknown_command(event, line_bot_api)


