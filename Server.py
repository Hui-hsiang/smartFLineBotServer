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
import random
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
        if (text=="金融小知識"):
            case = random.randint(0,6)
            reply_text = str(case)
            if case == 1:
                reply_text += "超額投保:\n超額投保是指投保的保險金額超過被保險人的可保價值、或是超過要保人繳費能力的保額。"
            elif case == 2:
                reply_text = "利率變動型年金:\n"
                reply_text += "與傳統型年金最大差異包括：\n"
                reply_text += "（1）透明化的年金帳戶餘額計算方式，每個扣除項目與累加項目均有明確的交代。\n"
                reply_text += "（2）定期、不定期、主動或被動提供客戶對帳單。\n"
                reply_text += "（3）可不定期不定額繳付保費。\n"
                reply_text += "（4）充分反應市場基本報酬率之波動（採宣告利率制）。在年金開始給付前，年金帳戶餘額受繳費頻率，每次繳費金額及每次宣告利率的高低而影響餘額之大小，換言之是非保證之金額，至於年金開始給付後所換算成之每次可領取年金金額是固定或變動的則視保戶所選擇的給付方式而定，可選擇每年領取固定年金金額或選擇領取同樣受每次宣告利率高低而影響其金額之變動年金金額。"
            elif case == 3:
                reply_text += "不足額保險:\n不足額保險是指被保險人的保單保額遠低於實際需求，不能滿足個人生活或事業的需求。llo"
            elif case == 4:
                reply_text += "人身意外傷害保險\n保險人補償被保險人因意外事故所致殘廢、薪資收入損失、醫療費用支出以及被保險人之死亡等之保險，美國慣用。"
            elif case == 5:
                reply_text += "純保費淨保費:\n在保險中有數種不同定義\:所收取之保費，減去業務員佣金；\n"
                reply_text += "1.保費減去任何退還保費；\n"
                reply_text += "2.收保險成本，即所收保險費減去附加費用與安全準備；\n"
                reply_text += "3.保單的保費減去已付或預期紅利。\n"
            else:
                reply_text += "變額萬能保險:\n顧名思義，該險種混合了萬能保險的某些彈性特點與變額保險的投資彈性，其特點包括：\n"
                reply_text += "（1）在某限度內可自行決定每期之保費支付金額。\n"
                reply_text += "（2）任意選擇調高或降低保額，但仍受最低保額之限制。\n"
                reply_text += "（3）保單持有人自行承擔投資風險。\n"
                reply_text += "（4）其現金價值就像變額保險一樣會高低起伏，也可能會降低至零（如分帳帳戶投資結果不良者），此時若未再繳付保費該保單會因而失效。\n"
                reply_text += "（5）放在分離帳戶（SeparateAccount）中的基金被規定用以支援該基金來源的保單，與保險公司一般帳戶（GeneralAccount）的資產是分開的，故當保險公司遇到財務困難時，帳戶的分開可以對變額萬能保險之保單持有人提供另外的安全邊際。\n"
            
            if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            
        elif(text=="金融產品"):
            carousel_template_message = TemplateSendMessage(
                alt_text='理財小知識',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/hPD89TI.png',
                            title='💰保險產品',
                            text='包含了人身保險以及財產保險，請於下方點選欲查詢之保險產品分類',
                            actions=[
                                URIAction(
                                    label='人身保險',
                                    uri='line://app/1653886666-7oZWKRLr'
                                )
                                URIAction(
                                    label='財產保險',
                                    uri='line://app/1653886666-7oZWKRLr'
                                )

                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                            title='💹證券商品',
                            text='包含了股票、基金與衍生性金融商品，於下方點選欲查詢之商品分類。',
                            actions=[
                                URIAction(
                                    label='股票',
                                    uri='line://app/1653886666-zqljLkA7'
                                )
                                URIAction(
                                    label='基金'',
                                    uri='line://app/1653886666-zqljLkA7'
                                )
                                URIAction(
                                    label='衍生性金融商品,
                                    uri='line://app/1653886666-zqljLkA7'
                                )

                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, carousel_template_message)

        else:
            reply_text = text
            reply_text = "Hi\n我是智能金融導購平台💼\n"
            reply_text += "有任何金融相關的問題都可以詢問我喔！\n"
            reply_text += "我會幫你轉接專業證券營業員與保險業務員\n"
            reply_text += "他們能幫你做詳細的介紹與申購👍"
            if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)

    

    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)