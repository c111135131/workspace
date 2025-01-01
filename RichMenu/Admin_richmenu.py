import requests
import json
from dotenv import load_dotenv
import os
from delete_RichMenu import delete_richMenu

# 載入環境變數
load_dotenv()

# LINE Channel Access Token 和目標使用者 ID
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')  # 特定使用者的 LINE User ID

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
    exit()

# 圖片路徑
image_path = 'C:\\Users\\user\\workspace\\RichMenu\\Admin_richMenu.png'

# 設置圖片上傳的 headers
headers_image = {
    'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}',
    'Content-Type': 'image/png'
}

# 打開圖片並發送 POST 請求
with open(image_path, 'rb') as image_file:
    image_data = image_file.read()
    response = requests.post(
        f'https://api-data.line.me/v2/bot/richmenu/{richmenu_id}/content',
        headers=headers_image,
        data=image_data
    )

# 檢查圖片上傳回應
if response.status_code == 200:
    print(f"成功上傳圖片到 Rich Menu {richmenu_id}")
else:
    print(f"錯誤：{response.status_code}, {response.text}")
    exit()

# 綁定 Rich Menu 給特定使用者
url = f'https://api.line.me/v2/bot/user/{ADMIN_ID}/richmenu/{richmenu_id}'
response = requests.post(url, headers={'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'})

# 檢查綁定回應
if response.status_code == 200:
    print(f"成功將 Rich Menu 綁定到使用者 {ADMIN_ID}")
else:
    print(f"錯誤：{response.status_code}, {response.text}")


#刪除
delete_richMenu(richmenu_id, CHANNEL_ACCESS_TOKEN)