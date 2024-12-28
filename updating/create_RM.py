import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# LINE Channel Access Token
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# 設置 headers
headers = {
    'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# Rich Menu JSON 配置
richmenu_json = {
    "size": {
      "width": 2500,
      "height": 1686
    },
    "selected": True,
    "name": "圖文選單 1",
    "chatBarText": "查看更多資訊",
    "areas": [
      {
        "bounds": {
          "x": 0,
          "y": 5,
          "width": 1255,
          "height": 829
        },
        "action": {
          "type": "message",
          "text": "下訂單"
        }
      },
      {
        "bounds": {
          "x": 1245,
          "y": 10,
          "width": 1255,
          "height": 829
        },
        "action": {
          "type": "message",
          "text": "菜單資訊"
        }
      },
      {
        "bounds": {
          "x": 0,
          "y": 827,
          "width": 1255,
          "height": 829
        },
        "action": {
          "type": "message",
          "text": "購買須知"
        }
      },
      {
        "bounds": {
          "x": 1245,
          "y": 827,
          "width": 1255,
          "height": 829
        },
        "action": {
          "type": "message",
          "text": "售後問題"
        }
      }
    ]
  }

# 上傳 Rich Menu 配置
response = requests.post('https://api.line.me/v2/bot/richmenu', headers=headers, data=json.dumps(richmenu_json))

# 檢查回應
if response.status_code == 200:
    richmenu_id = response.json()['richMenuId']
    print(f"成功創建 Rich Menu，ID: {richmenu_id}")
else:
    print(f"錯誤：{response.status_code}, {response.text}")

image_path = 'C:\\Users\\user\\workspace\\updating\\richMenu.png'

# 設置請求的 headers
headers = {
    'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}',
    'Content-Type': 'image/png'  # 設置圖片格式
}

# 打開圖片並發送 POST 請求
with open(image_path, 'rb') as image_file:
    response = requests.post(
        f'https://api-data.line.me/v2/bot/richmenu/{richmenu_id}/content',
        headers=headers,
        files={'file': image_file}
    )

# 檢查回應狀態
if response.status_code == 200:
    print(f"成功上傳圖片到 Rich Menu {richmenu_id}")
else:
    print(f"錯誤：{response.status_code}, {response.text}")