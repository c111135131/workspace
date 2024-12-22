from linebot.models import TextMessage
from database import get_unprocessed_orders, get_sales_report

# 管理員指令處理器
def handle_admin_command(event, line_bot_api):
    user_message = event.message.text.lower()

    if "未處理訂單" in user_message:
        orders = get_unprocessed_orders()
        if orders:
            reply = "\n".join([f"訂單ID: {o['id']}, 商品: {o['item_name']}, 數量: {o['quantity']}" for o in orders])
        else:
            reply = "目前沒有未處理的訂單。"

    elif "銷售報表" in user_message:
        report = get_sales_report()
        reply = "\n".join([f"{item}: {quantity}" for item, quantity in report.items()])

    else:
        reply = "未知的管理員指令，請輸入 '未處理訂單' 或 '銷售報表'。"

    # 發送回應給管理員
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=reply)
    )
