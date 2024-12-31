# Dessert Shop Line Bot

這是一個甜點店的 Line Bot 專案，旨在通過 Line 平台提供客戶服務，包括訂購甜點、查詢銷售報表和管理訂單等功能。

## 功能

### 客戶功能
- **新品推薦**：顯示新品推薦的甜點。
- **熱門甜點**：顯示熱門甜點。
- **菜單資訊**：顯示甜點菜單。
- **線上訂購**：客戶可以通過 Line Bot 訂購甜點。

### 管理員功能
- **未處理訂單**：顯示所有未處理的訂單。
- **銷售報表**：顯示當月的銷售報表。
- **發送完成訂單通知**：標記訂單為已完成並通知客戶。

## 安裝與配置

1. 克隆此專案到本地：
    ```bash
    git clone https://github.com/yourusername/dessert-shop-line-bot.git
    cd dessert-shop-line-bot
    ```

2. 創建並激活虛擬環境：
    ```bash
    python -m venv venv
    source venv/bin/activate  # 對於 Windows 用戶，使用 `venv\Scripts\activate`
    ```

3. 安裝所需的依賴：
    ```bash
    pip install -r requirements.txt
    ```

4. 創建 [.env](http://_vscodecontentref_/7) 文件並添加以下環境變量：
    ```
    LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
    LINE_CHANNEL_SECRET=your_line_channel_secret
    OPENAI_API_KEY=your_openai_api_key
    OPENAI_ENDPOINT=https://your_openai_endpoint.azure.com/
    SERVER_URL=https://your-server-url.com
    ```

## 運行應用

1. 啟動 Flask 應用：
    ```bash
    python app.py
    ```

2. 使用 ngrok 或其他工具將本地服務器暴露到互聯網：
    ```bash
    ngrok http 5000
    ```

3. 將 ngrok 提供的 URL 配置到 Line Developer Console 中的 Webhook URL。

## 文件說明

### [client.py](http://_vscodecontentref_/8)
處理客戶消息和訂單的邏輯。

### [admin.py](http://_vscodecontentref_/9)
處理管理員指令和訂單管理的邏輯。

### [database.py](http://_vscodecontentref_/10)
包含與資料庫交互的函數。

### [ai_reply.py](http://_vscodecontentref_/11)
使用 Azure OpenAI 生成回應的函數。

### [utils.py](http://_vscodecontentref_/12)
包含一些輔助函數，如驗證電話號碼、顯示菜單等。

### [app.py](http://_vscodecontentref_/13)
主應用文件，設置 Flask 應用和 Line Bot API，處理回調事件。

## 貢獻

歡迎提交問題和請求功能。如果您想貢獻代碼，請先 Fork 此倉庫，然後創建一個 Pull Request。

## 授權

此專案使用 MIT 授權。# Dessert Shop Line Bot

