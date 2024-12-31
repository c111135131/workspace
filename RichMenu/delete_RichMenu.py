import requests

def delete_richMenu(richmenu_id,CHANNEL_ACCESS_TOKEN):
  url = f'https://api.line.me/v2/bot/richmenu/{richmenu_id}'

  # 設置 headers
  headers = {
      'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
  }

  # 發送刪除請求
  response = requests.delete(url, headers=headers)

  # 檢查回應
  if response.status_code == 200:
      print(f"成功刪除 Rich Menu，ID: {richmenu_id}")
  else:
      print(f"錯誤：{response.status_code}, {response.text}")