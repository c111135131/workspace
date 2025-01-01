from linebot.models import *
import re
from database import get_completedOrder_client,mark_order_as_completed,get_unprocessed_orders,get_monthly_sales_report,save_order_to_db,select_OrderId
import qrcode
import os
import pandas as pd
import matplotlib.pyplot as plt

'''Admin.py'''

# 處理標記訂單為完成
def handle_order_completion(user_message, user_id, event, line_bot_api, user_sessions):
    try:
        # 驗證是否為有效的訂單ID（英文字母加數字）
        if re.match(r"^[A-Za-z0-9]+$", user_message):  # 假設ID僅由英文字母與數字組成
            order_id = user_message
            client_id = get_completedOrder_client(order_id)
            
            if client_id:
                # 標記訂單為完成並通知客戶
                mark_order_as_completed(order_id)
                line_bot_api.push_message(
                    client_id,
                    TextMessage(text=f"您的訂單 {order_id} 已完成，請到店取貨並付款。")
                )
                reply = f"訂單 {order_id} 已標記為完成並通知用戶。"
                user_sessions.pop(user_id, None)  # 清除會話狀態
            else:
                reply = f"訂單 {order_id} \n不存在或已完成。請確認輸入的ID。"
        elif user_message.strip().lower() == "取消":
            # 處理用戶取消操作
            user_sessions.pop(user_id, None)  # 清除會話狀態
            reply = "操作已取消。"
        else:
            reply = "請提供有效的訂單ID或輸入「取消」以退出操作。"
    except Exception as e:
        # 捕捉其他可能的錯誤
        reply = f"發生錯誤：{str(e)}"

    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))

# 顯示未處理訂單
def show_unprocessed_orders(event, line_bot_api, server):
    orders = get_unprocessed_orders()
    if orders:
        reply = "\n\n".join([f"訂單ID: {o['訂單編號']}, \n客戶名稱: {o['客戶名稱']}, \n客戶電話: {o['客戶電話']}, \n商品明細: {o['商品明細']}" for o in orders])
        line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))
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
def prompt_for_order_id(event, line_bot_api,user_sessions):
    uncompleted_orders = get_unprocessed_orders()
    if uncompleted_orders:
        reply = "未完成的訂單如下:\n\n"
        reply += "\n\n".join([f"訂單ID: {o['訂單編號']}, \n客戶名稱: {o['客戶名稱']}, \n客戶電話: {o['客戶電話']}, \n商品明細: {o['商品明細']}" for o in uncompleted_orders])
        reply += "\n\n請回覆要標記為完成的訂單ID。\n若不想繼續，請輸入「取消」。"
        # 設置會話狀態為等待訂單ID
        user_sessions[event.source.user_id] = "waiting_for_order_id"
    else:
        reply = "目前沒有未完成的訂單。"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))

# 處理未知指令
def reply_unknown_command(event, line_bot_api):
    reply = "未知的管理員指令，請輸入 '未處理訂單' 或 '銷售報表' 或 '發送完成訂單通知'。"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))


'''Client.py'''

# 檢查電話格式
def validate_phone_number(phone_number):
    pattern = re.compile(r"^\d{10}$")
    return pattern.match(phone_number) is not None

# 顯示文字訊息，提醒用戶輸入名字或電話
def request_name_and_phone(event, line_bot_api, user_id, user_data):
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text="請先輸入'您的名字'以完成註冊喔")
    )
    # 初始化用戶資料，並設置正在等待名字輸入
    user_data[user_id] = {"name": None, "phone": None, "waiting_for": "name"}

#展示菜單
def show_menu(event, line_bot_api):
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(
            thumbnail_image_url="https://image-cdn-flare.qdm.cloud/q625537188f5c0/image/data/2024/08/07/bfd529584f68c9603744b2adf1a6de74.jpg",
            title="草莓奶油蛋糕",
            text="NT$150\n新鮮草莓搭配香濃奶油，輕盈的蛋糕層次口感。",
            actions=[MessageAction(label="選擇草莓奶油蛋糕", text="草莓奶油蛋糕")]
        ),
        CarouselColumn(
            thumbnail_image_url="https://i.ytimg.com/vi/VBCw_Ua9HEA/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDDmwqmcuBFm74QyHqkev3M5iSs1g",
            title="巧克力慕斯",
            text="NT$180\n滑順的巧克力慕斯，濃郁的巧克力風味與絲滑口感。",
            actions=[MessageAction(label="選擇巧克力慕斯", text="巧克力慕斯")]
        ),
        CarouselColumn(
            thumbnail_image_url="https://makfahealth.com/upload/iblock/e9f/e9fe74c1d5a9b7010c19f756caa1ee5d.jpg",
            title="芒果椰漿布丁",
            text="NT$120\n芒果和椰漿製作的清爽布丁。",
            actions=[MessageAction(label="選擇芒果椰漿布丁", text="芒果椰漿布丁")]
        ),
        CarouselColumn(
            thumbnail_image_url="https://www.gomaji.com/blog/wp-content/uploads/2020/03/shutterstock_390854830-e1583823191128.jpg",
            title="檸檬塔",
            text="NT$130\n檸檬餡與酥脆塔皮的完美結合。",
            actions=[MessageAction(label="選擇檸檬塔", text="檸檬塔")]
        )
    ])
    template_message = TemplateSendMessage(
        alt_text="甜點菜單",
        template=carousel_template
    )
    line_bot_api.reply_message(event.reply_token, template_message)

#詢問數量
def ask_quantity(event, line_bot_api, user_id, item, orders):
    orders[user_id] = {"item": item}
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=f"您選擇的是 {item}，請輸入數量：")
    )

#確認訂單
def confirm_order(event, line_bot_api, user_id,orders):
    order = orders[user_id]
    item = order["item"]
    quantity = order["quantity"]
    total_price = int(quantity) * {"草莓奶油蛋糕": 150, "巧克力慕斯": 180, "芒果椰漿布丁": 120, "檸檬塔": 130}[item]
    
    buttons_template = ButtonsTemplate(
        title="確認訂單",
        text=f"您選擇的是：\n{item} x {quantity}\n總金額：NT${total_price}",
        actions=[
            PostbackAction(label="確認訂單", data="confirm_order"),
            PostbackAction(label="取消訂單", data="cancel_order")
        ]
    )
    template_message = TemplateSendMessage(
        alt_text="確認訂單",
        template=buttons_template
    )
    line_bot_api.reply_message(event.reply_token, template_message)

#處理客戶回傳訂單資訊
def handle_postback(event, line_bot_api,orders):
    user_id = event.source.user_id
    data = event.postback.data
    print(f"Received postback data: {data}")
    if data == "confirm_order":
        order = orders.pop(user_id)
        item = order["item"]
        quantity = order["quantity"]
        save_order_to_db(user_id, item, quantity)
        
        # 生成 QR Code
        # qr = qrcode.QRCode()
        # qr.add_data(f"訂單號碼：{orderId}")
        # qr.make()
        # img = qr.make_image(fill_color="black", back_color="white")
        # img.save('image/generated_qr_code.png', format="PNG")
        server = os.getenv('SERVER_URL')
        
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextMessage(text="感謝您的訂購！"),
                ImageSendMessage(original_content_url=f"{server}/generated_qr_code.png", preview_image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Desserts.jpg/640px-Desserts.jpg")
            ]
        )
        ADMIN_ID = os.getenv('ADMIN_ID')  # 請替換為實際的 admin 用戶 ID
        order_id = select_OrderId()
        admin_message = f"新訂單通知！\n訂單號碼：{order_id}\n品項：{item}\n數量：{quantity}"
        line_bot_api.push_message(ADMIN_ID, TextSendMessage(text=admin_message))

    elif data == "cancel_order":
        orders.pop(user_id, None)
        line_bot_api.reply_message(event.reply_token, TextMessage(text="訂單已取消，請重新訂購。"))
    else: 
        print(f"Unknown postback data: {data}")  # 錯誤處理