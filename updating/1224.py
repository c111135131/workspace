#markdown
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# 模擬甜點菜單
dessert_menu = {
    "1": {"name": "巧克力蛋糕", "price": 150},
    "2": {"name": "草莓慕斯", "price": 120},
    "3": {"name": "檸檬塔", "price": 100}
}

# 處理 LINE Webhook 請求
@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    try:
        events = json.loads(body)["events"]
        for event in events:
            if event['type'] == 'message' and event['message']['type'] == 'text':
                reply_token = event['replyToken']
                user_message = event['message']['text']
                reply_message = process_message(user_message)
                send_reply(reply_token, reply_message)
    except Exception as e:
        print(e)
    return 'OK'

# 處理使用者訊息
def process_message(user_message):
    if user_message.lower() == "menu":
        return format_menu()
    elif user_message.startswith("order"):
        return process_order(user_message)
    else:
        return "請輸入 'menu' 查看甜點菜單，或使用 'order [商品編號] [數量]' 進行訂購。"

# 格式化菜單為 Markdown
def format_menu():
    menu_md = "### 甜點菜單\n"
    for item_id, item in dessert_menu.items():
        menu_md += f"- **{item_id}. {item['name']}** - NT${item['price']}\n"
    return menu_md

# 處理訂單
def process_order(user_message):
    try:
        _, item_id, quantity = user_message.split()
        quantity = int(quantity)
        if item_id in dessert_menu:
            item = dessert_menu[item_id]
            total_price = item['price'] * quantity
            return (f"您已訂購 **{quantity} 份 {item['name']}**。\n"
                    f"總金額：**NT${total_price}**\n"
                    "感謝您的訂購！")
        else:
            return "無效的商品編號。請輸入 'menu' 查看甜點菜單。"
    except ValueError:
        return "訂購格式錯誤。請使用 'order [商品編號] [數量]' 進行訂購。"

# 發送回覆訊息
def send_reply(reply_token, reply_message):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_CHANNEL_ACCESS_TOKEN'
    }
    data = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": reply_message
        }]
    }
    requests.post(url, headers=headers, data=json.dumps(data))

if __name__ == "__main__":
    app.run(debug=True)