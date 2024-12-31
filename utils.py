from linebot.models import *
import re
import random
from database import save_order_to_db
import qrcode
import os
'''Admin.py'''


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
        num = str(random.randint(111*11,12345**9))
        orderId = user_id + num
        print(orderId)
        save_order_to_db(orderId, user_id, item, quantity)
        
        # 生成 QR Code
        qr = qrcode.QRCode()
        qr.add_data(f"訂單號碼：{orderId}")
        qr.make()
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('image/generated_qr_code.png', format="PNG")
        server = os.getenv('SERVER_URL')
        
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextMessage(text="感謝您的訂購！"),
                ImageSendMessage(original_content_url=f"{server}/generated_qr_code.png", preview_image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Desserts.jpg/640px-Desserts.jpg")
            ]
        )
        ADMIN_ID = os.getenv('ADMIN_ID')  # 請替換為實際的 admin 用戶 ID
        admin_message = f"新訂單通知！\n訂單號碼：{orderId}\n品項：{item}\n數量：{quantity}"
        line_bot_api.push_message(ADMIN_ID, TextSendMessage(text=admin_message))

    elif data == "cancel_order":
        orders.pop(user_id, None)
        line_bot_api.reply_message(event.reply_token, TextMessage(text="訂單已取消，請重新訂購。"))
    else: 
        print(f"Unknown postback data: {data}")  # 錯誤處理