import re
from linebot.models import *
from database import check_clientId, save_user_to_database, save_order_to_db
from ai_reply import handle_customer_service
import qrcode
import random
from io import BytesIO

user_data = {}
orders = {}

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

def show_menu(event, line_bot_api):
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(
            thumbnail_image_url="https://example.com/strawberry.jpg",
            title="草莓奶油蛋糕",
            text="NT$150\n新鮮草莓搭配香濃奶油，輕盈的蛋糕層次口感。",
            actions=[MessageAction(label="選擇草莓奶油蛋糕", text="草莓奶油蛋糕")]
        ),
        CarouselColumn(
            thumbnail_image_url="https://example.com/chocolate.jpg",
            title="巧克力慕斯",
            text="NT$180\n滑順的巧克力慕斯，濃郁的巧克力風味與絲滑口感。",
            actions=[MessageAction(label="選擇巧克力慕斯", text="巧克力慕斯")]
        ),
        CarouselColumn(
            thumbnail_image_url="https://example.com/mango.jpg",
            title="芒果椰漿布丁",
            text="NT$120\n芒果和椰漿製作的清爽布丁。",
            actions=[MessageAction(label="選擇芒果椰漿布丁", text="芒果椰漿布丁")]
        ),
        CarouselColumn(
            thumbnail_image_url="https://example.com/lemon.jpg",
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

def ask_quantity(event, line_bot_api, user_id, item):
    orders[user_id] = {"item": item}
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=f"您選擇的是 {item}，請輸入數量：")
    )

def confirm_order(event, line_bot_api, user_id):
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

def handle_postback(event, line_bot_api):
    user_id = event.source.user_id
    data = event.postback.data
    
    if data == "confirm_order":
        order = orders.pop(user_id)
        item = order["item"]
        quantity = order["quantity"]
        num = random.randint(111*11,12345**9)
        orderId = user_id + str(num)
        save_order_to_db(orderId, user_id, item, quantity)
        
        # 生成 QR Code
        qr = qrcode.QRCode()
        qr.add_data(f"訂單號碼：{orderId}")
        qr.make()
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextMessage(text="感謝您的訂購！"),
                ImageSendMessage(original_content_url="https://example.com/generated_qr_code.png", preview_image_url="https://example.com/generated_qr_code.png")
            ]
        )
    elif data == "cancel_order":
        orders.pop(user_id, None)
        line_bot_api.reply_message(event.reply_token, TextMessage(text="訂單已取消，請重新訂購。"))

def handle_client_message(event, line_bot_api):
    user_message = event.message.text.strip()
    user_id = event.source.user_id

    if check_clientId(user_id):
        if user_id in orders and "quantity" not in orders[user_id]:
            if user_message.isdigit():
                orders[user_id]["quantity"] = int(user_message)
                confirm_order(event, line_bot_api, user_id)
            else:
                line_bot_api.reply_message(event.reply_token, TextMessage(text="請輸入正確的數字作為數量。"))
        elif "線上訂購" in user_message:
            show_menu(event, line_bot_api)
        elif user_message in ["草莓奶油蛋糕", "巧克力慕斯", "芒果椰漿布丁", "檸檬塔"]:
            ask_quantity(event, line_bot_api, user_id, user_message)
        else:
            reply = handle_customer_service(user_message)
            line_bot_api.reply_message(event.reply_token, TextMessage(text=reply))
    else:
        if user_id not in user_data:
            request_name_and_phone(event, line_bot_api, user_id)
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