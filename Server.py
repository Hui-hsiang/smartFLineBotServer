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
import requests
import json
################################

from linebot.models import *

app = Flask(__name__)

class states(Enum):
    START = 0
    QUSTION = 1
    DIV = 2
    UNLOGIN = 3
    LOGIN = 4
class User():
    def __init__(self, id):
        self.user_id = id
        self.state = states.START
        self.quastionCount = 0
        self.div_id = 0
        self.identity = 0
        
selling = User('U2649922b5604a80e08b0f9dba91f9029')
selling.identity = 1
Users = [selling]


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

@handler.add(PostbackEvent)
def handle_post_message(event):
# can not get event text
    u = User(event.source.user_id)
    for i in Users:
        if i.user_id == event.source.user_id:
            u = i 
            

    if event.postback.data == 'apple':
        if selling.state != states.LOGIN:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(
                        text="營業員目前無法回覆您訊息\n",
                    )
                )
        
        else:
            selling.state = states.DIV
            u.div_id = 'U2649922b5604a80e08b0f9dba91f9029'
            u.state = states.DIV
            line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(
                        text="正在幫您導向營業員",
                    )
                )
            line_bot_api.push_message(
                            u.div_id,
                            TextMessage(
                                text="有新用戶想向您詢問問題",
                            )
                        )
            
            selling.div_id = u.user_id

    if event.postback.data == 'maggie':

        line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(
                        text="正在幫您導向營業員",
                    )
                )
        line_bot_api.push_message(
                        i.div_id,
                        TextMessage(
                            text="有新用戶想向您詢問問題",
                        )
                    )
    if event.postback.data == 'jerry':

        line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(
                        text="正在幫您導向營業員",
                    )
                )
        line_bot_api.push_message(
                        i.div_id,
                        TextMessage(
                            text="有新用戶想向您詢問問題",
                        )
                    )


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text=event.message.text
    
    f = False
    u = User(event.source.user_id)
    for i in Users:
        if i.user_id == event.source.user_id:
            u = i
            f = True
            break

    if (f == False):
        Users.append(u)
    if u.identity == 0:
        if u.state == states.START :
            if (text=="金融小知識"):
                case = random.randint(0,6)
                reply_text = ""
                if case == 1:
                    reply_text += "超額投保:\n超額投保是指投保的保險金額超過被保險人的可保價值、或是超過要保人繳費能力的保額。"
                elif case == 2:
                    reply_text += "利率變動型年金:\n"
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
                    alt_text='金融產品',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/hPD89TI.png',
                                title='💰保險產品',
                                text='包含了人身保險以及財產保險，請於下方點選欲查詢之保險產品分類',
                                actions=[
                                    MessageAction(
                                        label = '人身保險',
                                        text = '人身保險'
                                    ),
                                    MessageAction(
                                        label = '財產保險',
                                        text = '財產保險'
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='💹證券商品',
                                text='包含了股票、基金與衍生性金融商品，於下方點選欲查詢之商品分類。',
                                actions=[
                                    MessageAction(
                                        label = '股票',
                                        text = '股票'
                                    ),
                                    MessageAction(
                                        label = '基金',
                                        text = '基金'
                                    )
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
            elif(text=="人身保險"):
                carousel_template_message = TemplateSendMessage(
                    alt_text='人身保險',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='👫人身保險',
                                text='人身保險是以人的壽命和身體為保險標的的一種保險。',
                                actions=[
                                    MessageAction(
                                        label = '人壽保險',
                                        text = '人壽保險'
                                    ),
                                    MessageAction(
                                        label = '意外保險',
                                        text = '意外保險'
                                    ),
                                    MessageAction(
                                        label = '健康保險',
                                        text = '健康保險'
                                    )
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
            elif(text=="意外保險"):
                reply_text = "EY不EY"
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
            elif(text=="健康保險"):
                reply_text = "健康的保險非常重要喔"
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
            elif(text=="人壽保險"):
                carousel_template_message = TemplateSendMessage(
                    alt_text='人壽保險',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='👫人壽保險',
                                text='人壽保險產品',
                                actions=[
                                    MessageAction(
                                        label = '幸福轉蛋保險',
                                        text = '幸福轉蛋保險'
                                    ),
                                    MessageAction(
                                        label = '雋享年年終身保險',
                                        text = '雋享年年終身保險'
                                    ),
                                    MessageAction(
                                        label = '微馨愛小額終身壽險',
                                        text = '微馨愛小額終身壽險'
                                    )
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
            elif(text=="幸福轉蛋保險"):
                reply_text = "幸福轉蛋保險:\n\t商品特色\n"
                reply_text += "承保年齡：21 - 45歲\n"
                reply_text += "低保費擁有高保障\n"
                reply_text += "提供終身型別變更權，鎖住優良體況與未來保費\n"
                reply_text += "享有滿期金或生存金，回饋定期型年繳保險費\n"
                reply_text += "給付項目\n"
                reply_text += "身故/完全失能給付\n"
                reply_text += "生存金\n"
                reply_text += "祝壽金\n"
                reply_text += "滿期金\n"
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
            elif(text=="雋享年年終身保險"):
                reply_text = "沒有"
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
            elif(text=="微馨愛小額終身壽險"):
                reply_text = "也沒有"
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
            elif "投資方案" in text:
                carousel_template_message = TemplateSendMessage(
                    alt_text='人壽保險',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='請填問券',
                                text='麻煩您先填寫此風險屬性分析問卷，藉由您的答覆您會得知您的風險屬性，我也會幫您找到最合適的營業員，提供專業知識😃',
                                actions=[
                                    MessageAction(
                                        label = '投資風險屬性分析問卷',
                                        text = '投資風險屬性分析問卷'
                                    )
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
            elif text == "投資風險屬性分析問卷":
                u.state = states.QUSTION
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='一、請問您投資金融商品最主要的考量因素為何？',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action = MessageAction(label = '追求總投資報酬最大',text = '追求總投資報酬最大')
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="賺取資本利得", text="賺取資本利得")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="賺取固定的利息收益", text="賺取固定的利息收益")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="保本", text="保本")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="保持資產的流動性", text="保持資產的流動性")
                            )
                        ])))
                u.quastionCount += 1

            else:

                reply_text = "Hi\n我是智能金融導購平台💼\n"
                reply_text += "有任何金融相關的問題都可以詢問我喔！\n"
                reply_text += "我會幫你轉接專業證券營業員與保險業務員\n"
                reply_text += "他們能幫你做詳細的介紹與申購👍"
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
        
        elif u.state == states.QUSTION :
            if u.quastionCount == 1:
                u.quastionCount += 1
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='二、假設您有 NT100 萬元之投資組合，請問您可承擔最大本金下跌幅度為何？',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action = MessageAction(label = '0%',text = '0%')
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="-5%", text="-5%")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="-10%", text="-10%")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="-15%", text="-15")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="-20%以上", text="-20%以上")
                            )
                        ])))
            elif u.quastionCount == 2:
                u.quastionCount += 1
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='九、如您持有之整體投資資產下跌超過 15%，請問對您的生活影響程度為何？',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action = MessageAction(label = '無法承受',text = '無法承受')
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="中度影響", text="中度影響")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="影響程度小", text="影響程度小")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="沒有影響", text="沒有影響")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="影響程度大", text="影響程度大")
                            )
                        ])))
            elif u.quastionCount == 3:
                u.quastionCount += 1
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='十、當您的投資組合預期平均報酬率達到多少時才會考慮賣出？',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action = MessageAction(label = '25%以上',text = '25%以上')
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="20%", text="20%")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="15%", text="15%")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="10%", text="10%")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="5%", text="5%")
                            )
                        ])))
            else:
                u.state = states.START
                reply_text = "恭喜您完成問卷，經過分析後您的風險屬性為：【穩健型】\n"
                reply_text += "代表您可以接受中等的投資風險，希望預期報酬率可以優於長期存款利率；以期投資本金不因通貨膨脹而貶值，您可以接受高一點程度的波動。\n"
                
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                
                reply_text = "我已幫您找到了幾個證券營業員，我會將方才的投資屬性表及數據交給您所選擇的營業員，您可以更深入的向他們詢問相關問題😉\n"
                
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.push_message(event.source.user_id, TextSendMessage(text=reply_text))

                carousel_template_message = TemplateSendMessage(
                    alt_text='營業員',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='👔營業員 嘉禾',
                                text='您好，我是嘉禾，擔任證券營業員已有10年經歷，希望能用我的專業為您服務 !😁',
                                actions=[
                                    MessageAction(
                                        label = '查看評價',
                                        text = '查看評價'
                                    ),
                                    PostbackTemplateAction(
                                        label = '諮詢',
                                        data='jerry'
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='👔營業員 麥基',
                                text='您好，我是麥基，有8年證券業資歷，很高興能為您服務。👍',
                                actions=[
                                    MessageAction(
                                        label = '查看評價',
                                        text = '查看評價'
                                    ),
                                    PostbackTemplateAction(
                                        label = '諮詢',
                                        data='maggie'
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='👔營業員 曉琪',
                                text='您好，我是曉琪，我在證券業界服務5年了喔，很高興能為您服務!😉',
                                actions=[
                                    MessageAction(
                                        label = '查看評價',
                                        text = '查看評價'
                                    ),
                                    PostbackTemplateAction(
                                            label='諮詢', 
                                            data='apple'
                                        ),
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.push_message(event.source.user_id, carousel_template_message)
        elif u.state == states.DIV:
            if text == "離開":
                reply_text = "您已離開對話"

                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方已離開對話",
                        )
                    )
                for i in Users:
                    if i.user_id == u.div_id:
                        i.state = states.LOGIN
                        break
                u.state =states.START
            else:
                line_bot_api.push_message(u.div_id, TextSendMessage(text=text))
    else:
        if u.state == states.START:

            reply_text = "請輸入【手機號碼】登入系統"

            if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            u.state = states.UNLOGIN
        elif u.state == states.UNLOGIN:
            if(text == "確認"): 
                reply_text = "歡迎登入\n請點選下方【服務項目】執行動作"
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                u.state = states.LOGIN
                headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json","Content-Type":"application/json"}

                req = requests.request('POST', ' https://api.line.me/v2/bot/user/' + u.user_id + '/richmenu/' + 'richmenu-9a3e9e8fd2ca493c4b6c1c638ea5304d', 
                       headers=headers)
            elif(text == "修改"):
                reply_text = "輸入【手機號碼】登入系統"
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                carousel_template_message = TemplateSendMessage(
                    alt_text="請確認手機號碼是否正確：",
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/hPD89TI.png',
                                title='請確認手機號碼是否正確：',
                                text="【" + text + "】",
                                actions=[
                                    MessageAction(
                                        label = '確認',
                                        text = '確認'
                                    ),
                                    MessageAction(
                                        label = '修改',
                                        text = '修改'
                                    )
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
        elif u.state == states.LOGIN:
            if text == "登出":
                reply_text = "您已成功登出"

                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                
                u.state = states.START
                headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json","Content-Type":"application/json"}
                req = requests.request('POST', ' https://api.line.me/v2/bot/user/' + u.user_id + '/richmenu/' + 'richmenu-6b8167a5a521e96c320ca94ad954e6c6', 
                        headers=headers)

        elif u.state == states.DIV :
            if text == "離開":
                reply_text = "您已離開對話"

                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方已離開對話",
                        )
                    )
                for i in Users:
                    if i.user_id == u.div_id:
                        i.state = states.START
                        break
                u.state = states.LOGIN
            else:

                if (u.div_id != 0):
                    line_bot_api.push_message(
                            u.div_id,
                            TextMessage(
                                text=text,
                            )
                        )

    
    

    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    