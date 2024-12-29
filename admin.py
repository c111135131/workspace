from linebot.models import *
from database import get_unprocessed_orders, get_monthly_sales_report, get_completedOrder_client, mark_order_as_completed 
import pandas as pd
import matplotlib.pyplot as plt
import os

# 用來存儲管理員的會話狀態
user_sessions = {}

# 管理員指令處理器
def handle_admin_command(event, line_bot_api):
    user_message = event.message.text.lower()
    user_id = event.source.user_id  # 確保每個管理員的指令對應到正確的會話
    server = 'https://0b53-2402-7500-a72-1a93-cc07-44f9-d03a-fed4.ngrok-free.app'

    # 管理員會話狀態管理
    if user_id in user_sessions:
        session_state = user_sessions[user_id]
    else:
        session_state = None

    if session_state == "waiting_for_order_id":
        handle_order_completion(user_message, user_id, event, line_bot_api)
    elif "未處理訂單" in user_message:
        show_unprocessed_orders(event, line_bot_api, server)
    elif "銷售報表" in user_message:
        show_sales_report(event, line_bot_api, server)
    elif "發送完成訂單通知" in user_message:
        prompt_for_order_id(event, line_bot_api)
    else:
        reply_unknown_command(event, line_bot_api)

# 處理標記訂單為完成
def handle_order_completion(user_message, user_id, event, line_bot_api):
    try:
        order_id = int(user_message)  # 嘗試將訊息轉為訂單ID
        client_id = get_completedOrder_client(order_id)
        if client_id:
            mark_order_as_completed(order_id)
            line_bot_api.push_message(
                client_id,
                TextMessage(text=f"您的訂單 {order_id} 已完成，請到店取貨並付款。")
            )
            reply = f"訂單 {order_id} 已標記為完成並通知用戶。"
            user_sessions.pop(user_id)  # 結束此次會話
        else:
            reply = f"訂單 {order_id} 不存在或已完成。請輸入有效的訂單ID。"
    except ValueError:
        reply = "請提供有效的訂單ID。"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))

# 顯示未處理訂單
def show_unprocessed_orders(event, line_bot_api, server):
    orders = get_unprocessed_orders()
    if orders:
        os.makedirs("image", exist_ok=True)
        df = pd.DataFrame(orders)
        # 設定表格樣式
        fig, ax = plt.subplots(figsize=(10, len(df) * 0.5 + 1))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.2)
        # 保存表格為圖片
        image_path = 'image/unprocessed_orders.png'
        plt.savefig(image_path, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        # 發送圖片消息
        image_message = ImageSendMessage(
            original_content_url=f'{server}/image/unprocessed_orders.png',
            preview_image_url=f'{server}/image/unprocessed_orders.png'
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    else:
        reply = "目前沒有未處理的訂單。"
        line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))

# 顯示銷售報表
def show_sales_report(event, line_bot_api, server):
    dates, quantities = get_monthly_sales_report()
    os.makedirs("image", exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(dates, quantities, marker='o', color='b', linestyle='-', linewidth=2, markersize=5)
    plt.title("Monthly Sales Report", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Sales Quantity", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    image_path = "image/monthly_sales_report.png"
    plt.savefig(image_path)
    plt.close()
    image_message = ImageSendMessage(
        original_content_url=f'{server}/image/monthly_sales_report.png',
        preview_image_url=f'{server}/image/monthly_sales_report.png'
    )
    line_bot_api.reply_message(event.reply_token, image_message)

# 提示管理員輸入訂單ID
def prompt_for_order_id(event, line_bot_api):
    uncompleted_orders = get_unprocessed_orders()
    if uncompleted_orders:
        reply = "未完成的訂單如下:\n"
        reply += "\n".join([f"訂單ID: {o['訂單編號']}, 客戶名稱: {o['客戶名稱']}, 商品明細: {o['商品明細']}" for o in uncompleted_orders])
        reply += "\n請回覆要標記為完成的訂單ID。"
        # 設置會話狀態為等待訂單ID
        user_sessions[event.source.user_id] = "waiting_for_order_id"
    else:
        reply = "目前沒有未完成的訂單。"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))

# 處理未知指令
def reply_unknown_command(event, line_bot_api):
    reply = "未知的管理員指令，請輸入 '未處理訂單' 或 '銷售報表' 或 '發送完成訂單通知'。"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))
