import requests
import json
from dotenv import load_dotenv
import os
from delete_RichMenu import delete_richMenu

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
        "y": 0,
        "width": 1249,
        "height": 844
      },
      "action": {
        "type": "message",
        "text": "月銷售報表"
      }
    },
    {
      "bounds": {
        "x": 1251,
        "y": 0,
        "width": 1249,
        "height": 844
      },
      "action": {
        "type": "message",
        "text": "未處理訂單"
      }
    },
    {
      "bounds": {
        "x": 0,
        "y": 836,
        "width": 2499,
        "height": 844
      },
      "action": {
        "type": "message",
        "text": "發送完成訂單通知"
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

image_path = 'C:\\Users\\user\\workspace\\RichMenu\\richMenu.png'

# 設置請求的 headers
headers = {
    'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}',
    'Content-Type': 'image/png'  # 設置圖片格式
}

# 打開圖片並發送 POST 請求
with open(image_path, 'rb') as image_file:
    image_data = image_file.read()
    response = requests.post(
        f'https://api-data.line.me/v2/bot/richmenu/{richmenu_id}/content',
        headers=headers,
        data=image_data  # 將圖片內容作為 data 上傳
    )

# 檢查回應狀態
if response.status_code == 200:
    print(f"成功上傳圖片到 Rich Menu {richmenu_id}")
else:
    print(f"錯誤：{response.status_code}, {response.text}")

#刪除
# delete_richMenu(richmenu_id, CHANNEL_ACCESS_TOKEN)