from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from config import Config
from line_service import LineService
from chatgpt_service import ChatGPTService
from database import DatabaseManager

app = Flask(__name__)

line_service = LineService(Config.LINE_CHANNEL_ACCESS_TOKEN, Config.LINE_CHANNEL_SECRET)
chatgpt_service = ChatGPTService(Config.OPENAI_API_KEY)
db_manager = DatabaseManager(Config.DATABASE_PATH)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        line_service.handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/send_menu", methods=['GET'])
def send_menu():
    menu_message = line_service.create_dessert_menu_message()
    return "菜單已準備好"

@app.route("/place_order", methods=['POST'])
def place_order():
    # 訂單邏輯待實作
    pass

if __name__ == "__main__":
    app.run(port=5000)




