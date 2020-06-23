# Line Bot
from flask import Flask, request, abort
from urllib.request import urlopen
from config import line_channel_access_token, line_channel_secret
#from oauth2client.service_account import ServiceAccountCredentials
from enum import Enum
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)

################################

from linebot.models import *

app = Flask(__name__)

class states(Enum):
    START = 0

state = states.START



# Channel Access Token
line_bot_api = LineBotApi(line_channel_access_token)
# Channel Secret
handler = WebhookHandler(line_channel_secret)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text=event.message.text
    
    if state == states.START :
        if (text=="Hi"):
            reply_text = "Hello"
        elif(text=="你好"):
            reply_text = "哈囉"
        elif(text=="機器人"):
            reply_text = "叫我嗎"
        else:
            reply_text = text
            reply_text = "Hi\n我是智能金融導購平台💼\n"
            reply_text += "有任何金融相關的問題都可以詢問我喔！\n"
            reply_text += "我會幫你轉接專業證券營業員與保險業務員\n"
            reply_text += "他們能幫你做詳細的介紹與申購👍"

    
#如果非以上的選項，就會學你說話
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)