# Line Bot
from flask import Flask, request, abort, render_template
from urllib.request import urlopen
from config import line_channel_access_token, line_channel_secret
from datetime import date
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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('src/smartflinebotserver-firebase-adminsdk-q4kci-72696b6a64.json')

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore

db = firestore.client()


app = Flask(__name__)

class states(Enum):
    START = 0
    QUSTION = 1
    DIV = 2
    UNLOGIN = 3
    LOGIN = 4
    PETSQUSTION = 5
class User():
    def __init__(self, id):
        self.user_id = id
        self.state = states.START.value
        self.quastionCount = 0
        self.div_id = 0
        self.identity = 0
        self.name =""
        self.score = 0


def welcome_flex():
    
    content = {
        "type": "bubble",
        "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
            "type": "uri",
            "uri": "http://linecorp.com/"
            }
            },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "insurTech",
                "weight": "bold",
                "size": "xl"
                },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "嗨我是智慧金融導購平台 insurtech\n我能協助你喔",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                        }
                        ]
                    }
                ]
                }
                ]
            },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type":"message",
                    "label":"我想諮詢業務員",
                    "text":"我想諮詢業務員"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "uri",
                "label": "WEBSITE",
                "uri": "https://linecorp.com"
                }
            },
            {
                "type": "spacer",
                "size": "sm"
            }
            ],
            "flex": 0
            }
        }
    return content
def rank_flex():
    rank = 1
    today = date.today()
    user_sep = []
    docs = db.collection('sales').order_by('profit',direction=firestore.Query.DESCENDING).get()
    for i in docs:
        r_doc = i.to_dict()
        content = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "text",
                "text": "第" + str(rank) + "名",
                "size": "sm",
                "color": "#555555",
                "flex": 0
            }
            ]
        }
        user_sep.append(content)
        content = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "text",
                "text": "業務員: " + r_doc["name"],
                "size": "sm",
                "color": "#555555"
            }
            ]
        }
        user_sep.append(content)
        content = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "text",
                "text": "分潤金額: " + str(r_doc["profit"]),
                "size": "sm",
                "color": "#555555"
            }
            ]
        }
        user_sep.append(content)
        content = {
            "type": "separator",
            "margin": "xxl"
        }
        user_sep.append(content)
        rank += 1


    contents ={
        "type": "bubble",
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": str(today),
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": "業績英雄榜",
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
        },
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": user_sep
        }
        ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
    }
    return contents 

def historyServices_flex(text, date,product): 
    
    contents ={
        "type": "bubble",
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "交易紀錄",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": text,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
        },
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": date,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": product,
                    "size": "sm",
                    "color": "#555555"
                }
                ]
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type":"postback",
                "label":"申請理賠",
                "data":"apply&"+text+"&"+date+"&"+product,
                "text":"申請理賠"
                }
            }
            ]
        }
        ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        }
    return contents    

def comment_flex(name, img_url, rank, docs, url):
    
    star_ico = []
    goldStar = {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                }
    grayStar =  {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                }
    score = {
                "type": "text",
                "text": str(rank),
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
            }
    
    for i in range(int(rank)):
        star_ico.append(goldStar)
    for i in range(5-int(rank)):
        star_ico.append(grayStar)
    star_ico.append(score)

    comment = []
    for i in docs:
        doc = i.to_dict()

        comment.append({
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "text",
                    "text": doc['name'],
                    "wrap": True,
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 2
                    },
                    {
                    "type": "text",
                    "text": doc['comment'],
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                    }
                ]
        })

    print (img_url)
    content = {
        "type": "bubble",
        "hero": {
        "type": "image",
        "url": img_url,
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
            "type": "uri",
            "uri": url
        }
        },
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
            "type": "text",
            "text": name,
            "weight": "bold",
            "size": "xl"
            },
            {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": star_ico
            },
            {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": comment 
            }
        ]
        },
        "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": "所有評論",
                "uri": url
            }
            },
            {
            "type": "spacer",
            "size": "sm"
            }
        ],
        "flex": 0
        }
    }
    return content

def UserData_get(id):
    path = "user/" + id
    collection_ref = db.document(path)
    doc = collection_ref.get()
    return doc.to_dict()

def UserData_new(id, profile):
    doc = { 
            'user_id' : id,
            'state' : 0,
            'quastionCount' : 0,
            'div_id' : "",
            'identity' : 0,
            'name' : profile.display_name,
            'score' : 0
        }
    db.collection("user").document(id).set(doc)
def message_new(id,message):
    db.collection("message").document(id).set(message)
def message_update(id,message):
    db.collection("message").document(id).update(message)
def toUser(doc):
    u = User(doc['user_id'])
    u.state = doc['state']
    u.quastionCount = doc['quastionCount']
    u.div_id = doc['div_id']
    u.identity = doc['identity']
    u.name = doc['name']
    u.score = doc['score']
    return u
def UserData_update(u,doc):
    db.collection("user").document(u.user_id).update(doc)

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

@app.route("/purchase", methods=['GET','POST'])
def purchase():
    if request.method == 'POST':
        return render_template("petForm.html")
    return render_template("petForm.html")

@app.route("/apply", methods=['GET','POST'])
def apply():
    if request.method == 'POST':
        return render_template("apply.html")
    if request.method == 'GET':
        name = request.args.get('name')
        date = request.args.get('date')
        product = request.args.get('product')
        return render_template("apply.html",name = name,date = date,product = product)    
    return render_template("apply.html")

@app.route("/001", methods=['GET'])
def lineFriends001():
    line_bot_api.push_message(
                        'U2649922b5604a80e08b0f9dba91f9029',
                        TextMessage(
                            text="有新用由寵物店001加入好友!",
                        )
                    )
    return render_template("lineFriends.html")
@app.route("/002", methods=['GET'])
def lineFriends002():
    line_bot_api.push_message(
                        'U2649922b5604a80e08b0f9dba91f9029',
                        TextMessage(
                            text="有新用由寵物店002加入好友!",
                        )
                    )
    return render_template("lineFriends.html")
@app.route("/003", methods=['GET'])
def lineFriends003():
    line_bot_api.push_message(
                        'U2649922b5604a80e08b0f9dba91f9029',
                        TextMessage(
                            text="有新用由寵物店003加入好友!",
                        )
                    )
    return render_template("lineFriends.html")
@app.route("/applecomments", methods=['GET','POST'])
def applecomments():
    
    posts = []
    names = []

    docs = db.collection('comment').where('id','==', 'U2649922b5604a80e08b0f9dba91f9029').get()
    s_doc = db.collection('sales').document('U2649922b5604a80e08b0f9dba91f9029').get().to_dict()


    for i in docs:
        i = i.to_dict()
        posts.append(i['comment'])
        names.append(i['name'])
    
    if request.method == 'POST':
        new_comment = {
            'id' : 'U2649922b5604a80e08b0f9dba91f9029',
            'star' : int(request.form.get('star')),
            'comment' : request.form.get('comment'),
            'name' : request.form.get('name'),
        }
        
        s_doc['serviceCount'] = s_doc['serviceCount'] + 1
        s_doc['score'] = s_doc['score'] + int(request.form.get('star'))
        posts.append(request.form.get('comment'))
        names.append(request.form.get('name'))
        db.collection('comment').add(new_comment)
        db.collection('sales').document('U2649922b5604a80e08b0f9dba91f9029').update(s_doc)
        return render_template("comments.html", title = 'apple', names = names, posts = posts)
    else:
        return render_template("comments.html", title = 'apple', names = names, posts = posts)

@app.route("/jerrycomments", methods=['GET','POST'])
def jerrycomments():
    
    posts = []
    names = []

    docs = db.collection('comment').where('id','==', 'U60d04b2a91c5b050242a42de2c1b1947').get()
    s_doc = db.collection('sales').document('U60d04b2a91c5b050242a42de2c1b1947').get().to_dict()


    for i in docs:
        i = i.to_dict()
        posts.append(i['comment'])
        names.append(i['name'])
    
    if request.method == 'POST':
        new_comment = {
            'id' : 'U60d04b2a91c5b050242a42de2c1b1947',
            'star' : int(request.form.get('star')),
            'comment' : request.form.get('comment'),
            'name' : request.form.get('name'),
        }
        
        s_doc['serviceCount'] = s_doc['serviceCount'] + 1
        s_doc['score'] = s_doc['score'] + int(request.form.get('star'))
        posts.append(request.form.get('comment'))
        names.append(request.form.get('name'))
        db.collection('comment').add(new_comment)
        db.collection('sales').document('U60d04b2a91c5b050242a42de2c1b1947').update(s_doc)
        return render_template("comments.html", title = 'jerry', names = names, posts = posts)
    else:
        return render_template("comments.html", title = 'jerry', names = names, posts = posts)


@handler.add(PostbackEvent)
def handle_post_message(event):
# can not get event text


    u_doc = UserData_get(event.source.user_id)
    u = toUser(u_doc)
    

    if event.postback.data == 'apple':
        s_doc = UserData_get('U2649922b5604a80e08b0f9dba91f9029')
        s = toUser(s_doc)

        message_doc = {
            'sales_id' : s.user_id
        }

        message_update(u.user_id,message_doc)
        reply_text = "您的問題已加入等候序列\n請耐心等候專員回復"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.push_message(
                        s.user_id,
                        TextMessage(
                            text="有新用戶想向您詢問問題",
                        )
                    )
        UserData_update(s,s_doc)

    elif event.postback.data == 'maggie':
        s_doc = UserData_get('U2649922b5604a80e08b0f9dba91f9029')
        s = toUser(s_doc)

        message_doc = {
            'sales_id' : s.user_id
        }

        message_update(u.user_id,message_doc)
        reply_text = "您的問題已加入等候序列\n請耐心等候專員回復"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.push_message(
                        s.user_id,
                        TextMessage(
                            text="有新用戶想向您詢問問題",
                        )
                    )
        UserData_update(s,s_doc)

    elif event.postback.data == 'jerry':

        s_doc = UserData_get('U60d04b2a91c5b050242a42de2c1b1947')
        s = toUser(s_doc)

        message_doc = {
            'sales_id' : s.user_id
        }

        message_update(u.user_id,message_doc)
        reply_text = "您的問題已加入等候序列\n請耐心等候專員回復"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.push_message(
                        s.user_id,
                        TextMessage(
                            text="有新用戶想向您詢問問題",
                        )
                    )
        UserData_update(s,s_doc)

    elif event.postback.data == 'commentapple':
        s_doc = db.collection('sales').document('U2649922b5604a80e08b0f9dba91f9029').get().to_dict()
        score = s_doc['score'] / s_doc['serviceCount']
        docs = db.collection("comment").where('id','==', 'U2649922b5604a80e08b0f9dba91f9029').get()
        url = 'https://smartflinebotserver.herokuapp.com/applecomments'
        content= comment_flex('apple',line_bot_api.get_profile('U2649922b5604a80e08b0f9dba91f9029').picture_url,score,docs,url)
        line_bot_api.reply_message(event.reply_token, line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage('評價', content)
                    )
                )
       
    elif event.postback.data == 'commentjerry':
        
        
        s_doc = db.collection('sales').document('U60d04b2a91c5b050242a42de2c1b1947').get().to_dict()
        score = s_doc['score'] / s_doc['serviceCount']
        docs = db.collection("comment").where('id','==', 'U60d04b2a91c5b050242a42de2c1b1947').get()
        url = 'https://smartflinebotserver.herokuapp.com/jerrycomments'
        content= comment_flex('嘉禾',line_bot_api.get_profile('U60d04b2a91c5b050242a42de2c1b1947').picture_url,score,docs,url)
        line_bot_api.reply_message(event.reply_token, line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage('評價', content)
                    )
                )
    elif event.postback.data == 'commentmaggie':
        reply_text = "營業員麥基目前沒有評價"
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)
    elif event.postback.data.split("&")[0] == 'apply':
        name = event.postback.data.split("&")[1]
        date = event.postback.data.split("&")[2]
        product = event.postback.data.split("&")[3]
        get_url = 'https://smartflinebotserver.herokuapp.com/apply?name='+name+'&date='+date+'&product='+product
        buttons_template_message = TemplateSendMessage(
        alt_text='申請理賠',
        template=ButtonsTemplate(
            title='點選申請' + product + "理賠",
            text='購買人姓名:' + name + '\n購買日期:' + date + '\n產品:' + product,
            actions=[
                URIAction(
                    label='前往申請',
                    uri=get_url
                )
            ]
        )
    )
            
        line_bot_api.reply_message(
            event.reply_token,
            buttons_template_message
            )




    elif u.state == states.QUSTION.value :
        if event.postback.data == 'a':
            u.score += 2
            u_doc["score"] = u.score
        elif event.postback.data == 'b':
            u.score += 4
            u_doc["score"] = u.score
        elif event.postback.data == 'c':
            u.score += 6
            u_doc["score"] = u.score
        elif event.postback.data == 'd':
            u.score += 8
            u_doc["score"] = u.score
        elif event.postback.data == 'e':    
            u.score += 10
            u_doc["score"] = u.score

        if u.quastionCount == 1:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='二、請問您的投資經驗為何?(投資經驗、時間)',
                quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='沒有經驗',
                                            display_text='沒有經驗',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='1-3年',
                                            display_text='1-3年',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='4-6年',
                                            display_text='4-6年',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='7-9年',
                                            display_text='7-9年',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='10年以上',
                                            display_text='10年以上',
                                            data='e'
                                        )
                            )
                    ])))
        elif u.quastionCount == 2:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='三、請問您曾經投資過那些金融商品?',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='台外幣存款、貨幣型基金、儲蓄型保險',
                                            display_text='台外幣存款、貨幣型基金、儲蓄型保險',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='債券、債券型基金',
                                            display_text='債券、債券型基金',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='股票、股票型基金、 ETF',
                                            display_text='股票、股票型基金、 ETF',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='結構型商品、投資型保單',
                                            display_text='結構型商品、投資型保單',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='期貨、選擇權或其他衍生性金融商品',
                                            display_text='期貨、選擇權或其他衍生性金融商品',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 3:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='四、請問您有多少年投資經驗在具價值波動性之商品(包括股票、共同基金、外幣、結構型投資商品、認(售)購權證、期貨、選擇權及投資型保單) ？(風險評估-偏好)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='沒有經驗',
                                            display_text='沒有經驗',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='1 〜 3 年',
                                            display_text='1 〜 3 年',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='4 〜 6 年',
                                            display_text='4 〜 6 年',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='7 〜 9 年',
                                            display_text='7 〜 9 年',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='10 年以上',
                                            display_text='10 年以上',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 4:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='五、請問您目前投資之資產中，約有多少比例是持有前述 2.4 所列舉之具價值波動性得商品 ？ (風險評估-偏好)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='0%',
                                            display_text='0%',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='介於 0%〜10%(含)',
                                            display_text='介於 0%〜10%(含)',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='介於 10%〜25%(含) ',
                                            display_text='介於 10%〜25%(含) ',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='介於 25%〜50%(含) ',
                                            display_text='介於 25%〜50%(含) ',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='超過 50%',
                                            display_text='超過 50%',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 5:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='六、在一般情況下，您所能接受之價格波動，大約在那種程度？ (風險評估-偏好)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='價格波動介於-5% 〜 +5%之間',
                                            display_text='價格波動介於-5% 〜 +5%之間',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='價格波動介於-10% 〜 +10%之間',
                                            display_text='價格波動介於-10% 〜 +10%之間',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='價格波動介於-15% 〜 +15%之間',
                                            display_text='價格波動介於-15% 〜 +15%之間',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='價格波動介於-20% 〜 +20%之間',
                                            display_text='價格波動介於-20% 〜 +20%之間',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='價格波動超過±20%',
                                            display_text='價格波動超過±20%',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 6:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='7、假設您有 NT100 萬元之投資組合，請問您可承擔最大本金下跌幅度為何？(風險評估- 承受力)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='0%',
                                            display_text='0%',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='-5% ',
                                            display_text='-5% ',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='-10%',
                                            display_text='-10%',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='-15%',
                                            display_text='-15%',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='-20%以上',
                                            display_text='-20%以上',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 7:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='八、如您持有之整體投資資產下跌超過 15%，請問對您的生活影響程度為何？(風險評估-承受力)(現金流量期望)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='無法承受',
                                            display_text='無法承受',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='影響程度大',
                                            display_text='影響程度大',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='中度影響',
                                            display_text='中度影響',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='影響程度小',
                                            display_text='影響程度小',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='沒有影響',
                                            display_text='沒有影響',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 8:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='九、當您的投資超過預設的停損或停利點時，請問您會採取那種處置方式？(風險評估-偏好) (現金流量期望)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='立即賣出所有部位',
                                            display_text='立即賣出所有部位',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='先賣出一半或一半以上部位',
                                            display_text='先賣出一半或一半以上部位',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='先賣出一半以內部位',
                                            display_text='先賣出一半以內部位',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='暫時觀望，視情況再因應(價差)',
                                            display_text='暫時觀望，視情況再因應(價差)',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='繼續持有至回本或不漲為止',
                                            display_text='繼續持有至回本或不漲為止',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 9:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='十、當您的投資組合預期平均報酬率達到多少時才會考慮賣出？(風險評估) (現金流量期望)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='5%',
                                            display_text='5%',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='10%',
                                            display_text='10%',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='15%',
                                            display_text='15%',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='20%',
                                            display_text='20%',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='25%以上',
                                            display_text='25%以上',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 10:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='十一、若有臨時且非預期之事件發生時，請問您的備用金相當於您幾個月的家庭開支？(備用金係指在沒有違約金的前提下可隨時動用的存款) (風險評估-承受力)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='無備用金儲蓄',
                                            display_text='無備用金儲蓄',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='3個月以下',
                                            display_text='3個月以下',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='3個月(含)以上〜6個月',
                                            display_text='3 個月(含)以上 〜 6 個月',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='6個月(含)以上〜9個月',
                                            display_text='6 個月(含)以上〜9個月',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='9個月(含)以上',
                                            display_text='9個月(含)以上',
                                            data='e'
                                        )
                            )
                ])))
        elif u.quastionCount == 11:
            u.quastionCount += 1
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
            text='十二、請問您偏好以下那類風險及報酬率之投資組合？(期望報酬)',
            quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='沒有概念',
                                            display_text='沒有概念',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='低度風險，只要保本就好',
                                            display_text='低度風險，只要保本就好',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='低風險承擔下，追求低的投資報酬',
                                            display_text='低風險承擔下，追求低的投資報酬',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='在中等風險承擔下，要求中等的合理報酬',
                                            display_text='在中等風險承擔下，要求中等的合理報酬',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='願意承擔高度風險，也期待創造超額報酬',
                                            display_text='願意承擔高度風險，也期待創造超額報酬',
                                            data='e'
                                        )
                            )
                ])))
        else:
            u.state = states.START.value
            u.quastionCount = 0
            if u.score>=20 and u.score <=27:
                reply_text = "恭喜您完成問卷，經過分析後您的風險屬性為：【保守型】\n"
                reply_text += "代表您能承受的資產波動風險極低。極度保守的您十分注重本金的保護，寧可讓資產隨著利率水準每年獲取穩定的孳息收入，也不願冒風險追求可能的可觀報酬。\n"
            elif u.score>=28 and u.score <=36:
                reply_text = "恭喜您完成問卷，經過分析後您的風險屬性為：【安穩型】\n"
                reply_text += "代表您能承受的資產波動風險低。除了注重本金的保護外，您願意承受有限的風險，以獲得比定存高的報酬。\n"
            elif u.score>=37 and u.score <=47:
                reply_text = "恭喜您完成問卷，經過分析後您的風險屬性為：【穩健型】\n"
                reply_text += "代表您能承受的資產波動風險中庸。穩健的您期望在本金、固定孳息與資本增長達致平衡。您可以接受短期間的市場波動，並且瞭解投資現值可能因而減損。\n"
            elif u.score>=48 and u.score <=60:
                reply_text = "恭喜您完成問卷，經過分析後您的風險屬性為：【成長型】\n"
                reply_text += "代表您能承受的資產波動風險高。為了達成長期的資本增長，您願意忍受較大幅度的市場波動與短期下跌風險。\n"
            else:
                reply_text = "恭喜您完成問卷，經過分析後您的風險屬性為：【積極型】\n"
                reply_text += "代表您能承受的資產波動風險極高。非常積極的您如獵鷹般不停尋找獲利市場，並願意大筆投資在風險屬性較高的商品。\n"

            line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(
                        text=reply_text,
                    )
                )
            reply_text = "我已幫您找到了幾個證券營業員，我會將方才的投資屬性表及數據交給您所選擇的營業員，您可以更深入的向他們詢問相關問題😉\n"
            line_bot_api.push_message(
                    event.source.user_id,
                    TextMessage(
                        text=reply_text,
                    )
                )
            carousel_template_message = TemplateSendMessage(
                alt_text='營業員',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/9PATfwz.jpg',
                            title='👔營業員 嘉禾',
                            text='您好，我是嘉禾，擔任證券營業員已有10年經歷，希望能用我的專業為您服務 !😁',
                            actions=[
                                PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentjerry'
                                        ),
                                PostbackTemplateAction(
                                    label = '諮詢',
                                    data='jerry'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/n06HVkC.jpg',
                            title='👔營業員 麥基',
                            text='您好，我是麥基，有8年證券業資歷，很高興能為您服務。👍',
                            actions=[
                                PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentmaggie'
                                        ),
                                PostbackTemplateAction(
                                    label = '諮詢',
                                    data='maggie'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/pDtoSWN.jpg',
                            title='👔營業員 曉琪',
                            text='您好，我是曉琪，我在證券業界服務5年了喔，很高興能為您服務!😉',
                            actions=[
                                PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentapple'
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
        u_doc["quastionCount"] = u.quastionCount
        u_doc["state"] = u.state 

    else:
        s_doc = UserData_get(event.postback.data)
        s = toUser(s_doc)
        s.state = states.DIV.value
        s_doc["state"] = s.state
        u.state = states.DIV.value
        u_doc["state"] = u.state
        s.div_id = event.source.user_id
        s_doc["div_id"] = s.div_id
        u.div_id = event.postback.data
        u_doc["div_id"] = u.div_id

        line_bot_api.reply_message(
                event.reply_token,
                TextMessage(
                    text="正在幫您導向該用戶",
                )
            )
        line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="專員已接受您的諮詢，正在幫您導向專員",
                        )
                    )
        path = "message/" + event.postback.data
        doc_ref = db.document(path)
        doc_ref.delete()
        UserData_update(s,s_doc)

    UserData_update(u,u_doc)


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text=event.message.text

    profile = line_bot_api.get_profile(event.source.user_id)
    doc = UserData_get(event.source.user_id)
    if  doc == None:
        UserData_new(event.source.user_id, profile)
        doc = UserData_get(event.source.user_id)

    u = toUser(doc)

    if u.identity == 0:

        if u.state == states.START.value :
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
                
                
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            elif '年齡' in text:
                reply_text = '保險年齡計算是以「足歲」來計算，生日超過6個月要加一歲。說明：保險年齡是以最近生日法來計算，即以是否超過六個月為準，並以申請投保日當天計算年齡，例：30足歲5個月又8天~30歲，30足歲6個月~30歲，30足歲6個月又1天~31歲。'
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            elif(text=="保險產品"):
                carousel_template_message = TemplateSendMessage(
                    alt_text='保險產品',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/DX0hJiE.png',
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
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/kdZovY5.png',
                                title='財產保險',
                                text='又名產物保險，是以各種財產及其相關利益為保險標的的保險。',
                                actions=[
                                    MessageAction(
                                        label = '住宅火險',
                                        text = '住宅火險'
                                    ),
                                    MessageAction(
                                        label = '寵物險',
                                        text = '寵物險'
                                    ),
                                    MessageAction(
                                        label = '汽車保險',
                                        text = '汽車保險'
                                    )                                   
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
            
            elif(text=="意外保險"):
                reply_text = "EY不EY"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            elif(text=="健康保險"):
                reply_text = "健康的保險非常重要喔"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            elif(text=="人壽保險"):
                carousel_template_message = TemplateSendMessage(
                    alt_text='人壽保險',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/Yge62eu.png',
                                title='👫人壽保險',
                                text='人壽保險產品',
                                actions=[
                                    MessageAction(
                                        label = '國泰人壽 幸福轉蛋保險',
                                        text = '國泰人壽 幸福轉蛋保險'
                                    ),
                                    MessageAction(
                                        label = '南山人壽 優活定期壽險',
                                        text = '南山人壽 優活定期壽險'
                                    ),
                                    MessageAction(
                                        label = '新光人壽 My Way定期壽險',
                                        text = '新光人壽 My Way定期壽險'
                                    )
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
            elif(text=="國泰人壽 幸福轉蛋保險"):
                reply_text = "幸福轉蛋保險:\n商品特色\n"
                reply_text += "承保年齡：21 - 45歲\n"
                reply_text += "低保費擁有高保障\n"
                reply_text += "提供終身型別變更權，鎖住優良體況與未來保費\n"
                reply_text += "享有滿期金或生存金，回饋定期型年繳保險費\n"
                reply_text += "給付項目\n"
                reply_text += "身故/完全失能給付\n"
                reply_text += "生存金\n"
                reply_text += "祝壽金\n"
                reply_text += "滿期金\n"
                
                image_message = ImageSendMessage(
                    original_content_url='https://i.imgur.com/fU0G3rU.png',
                    preview_image_url='https://i.imgur.com/fU0G3rU.png'
                )
                
                message = image_message
                line_bot_api.reply_message(event.reply_token, message)

                
            elif(text=="雋享年年終身保險"):
                reply_text = "雋享年年終身保險:\n商品特色\n"
                reply_text += "承保年齡(15年期)：0 - 65歲\n"
                reply_text += "承保年齡(20年期)：0 - 60歲\n"
                reply_text += "年年領取生存金，資金活用高\n"
                reply_text += "繳費期間高保障，繳費期滿高生存金\n"
                reply_text += "意外相關保障加倍至85歲前，揪安心\n"
                reply_text += "給付項目\n"
                reply_text += "生存保險金\n"
                reply_text += "祝壽保險金\n"
                reply_text += "身故保險金\n"
                reply_text += "完全失能保險金\n"
                
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            elif(text=="微馨愛小額終身壽險"):
                reply_text = "微馨愛小額終身壽險:\n商品特色\n"
                reply_text += "承保年齡(6年期)16 - 88歲\n"
                reply_text += "承保年齡(10年期)：16 - 82歲\n"
                reply_text += "承保年齡(15、20年期)：16 - 80歲\n"
                reply_text += "保費便宜保障終身\n"
                reply_text += "給付項目\n"
                reply_text += "身故保險金\n"
                reply_text += "完全失能保險金\n"
                reply_text += "祝壽金\n"
                
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            elif(text=="平台介紹"):
                image_message = ImageSendMessage(
                    original_content_url='https://imgur.com/A0E7Hwz.png',
                    preview_image_url='https://imgur.com/A0E7Hwz.png'
                )
                
                message = image_message
                line_bot_api.reply_message(event.reply_token, message)
            elif "投資方案" in text:
                message_doc = {
                    'message' : text,
                    'name' : profile.display_name,
                    'user_id' : u.user_id,
                    'sales_id' : ''
                }

                message_new(u.user_id,message_doc)

                if u.score ==0:
                    carousel_template_message = TemplateSendMessage(
                        alt_text='請填問卷',
                        template=CarouselTemplate(
                            columns=[
                                CarouselColumn(
                                    thumbnail_image_url='https://i.imgur.com/Y5OwYWV.png',
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
                else: 
                    reply_text = "我已幫您找到了幾個證券營業員，我會將方才的投資屬性表及數據交給您所選擇的營業員，您可以更深入的向他們詢問相關問題😉\n"
                    line_bot_api.push_message(
                            event.source.user_id,
                            TextMessage(
                                text=reply_text,
                            )
                        )
                    carousel_template_message = TemplateSendMessage(
                        alt_text='營業員',
                        template=CarouselTemplate(
                            columns=[
                                CarouselColumn(
                                    thumbnail_image_url='https://i.imgur.com/Hz8f9N3.jpg',
                                    title='👔營業員 嘉禾',
                                    text='您好，我是嘉禾，擔任證券營業員已有10年經歷，希望能用我的專業為您服務 !😁',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentjerry'
                                        ),
                                        PostbackTemplateAction(
                                            label = '諮詢',
                                            data='jerry'
                                        )
                                    ]
                                ),
                                CarouselColumn(
                                    thumbnail_image_url='https://i.imgur.com/n06HVkC.jpg',
                                    title='👔營業員 麥基',
                                    text='您好，我是麥基，有8年證券業資歷，很高興能為您服務。👍',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentmaggie'
                                        ),
                                        PostbackTemplateAction(
                                            label = '諮詢',
                                            data='maggie'
                                        )
                                    ]
                                ),
                                CarouselColumn(
                                    thumbnail_image_url='https://i.imgur.com/pDtoSWN.jpg',
                                    title='👔營業員 曉琪',
                                    text='您好，我是曉琪，我在證券業界服務5年了喔，很高興能為您服務!😉',
                                    actions=[
                                        PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentapple'
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
            elif text == "最新活動":
                carousel_template_message = TemplateSendMessage(
                    alt_text='最新活動1',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
#                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='目前尚未有任何最新活動',
                                text='待平台正式營運，將會更新最新活動',
                                actions=[
                                    MessageAction(
                                        label='最新活動',
                                        text='最新活動'
                                    ),
                                ]
                            )
                        ]
                    )
                )  
                line_bot_api.reply_message(event.reply_token, carousel_template_message)   
            elif text == "常見問題":
                carousel_template_message = TemplateSendMessage(
                    alt_text='常見問題',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/N8LSkzI.png',
                                title='該如何找尋投資方案建議',
                                text='建議使用者輸入「投資方案」等字元，平台會先提供投資風險屬性問卷填寫，了解使用者風險屬性係數，並推薦合適的營業員給使用者進行詢問',
                                actions=[
                                    MessageAction(
                                        label='我還有其他疑問',
                                        text='我還有其他疑問'
                                    ),
                                ]
                            )
                        ]
                    )
                )  
                line_bot_api.reply_message(event.reply_token, carousel_template_message)
            
            elif "諮詢" in text:
                u.state = states.PETSQUSTION.value
                doc["state"] = u.state

                message = ImagemapSendMessage(
                    base_url='https://i.imgur.com/rrffBB8.png',
                    alt_text='sex',
                    base_size=BaseSize(height=520, width=1040),
                    actions=[
                        MessageImagemapAction(
                            text='male',
                            area=ImagemapArea(
                                x=0, y=0, width=520, height=520
                            )
                        ),
                        MessageImagemapAction(
                            text='female',
                            area=ImagemapArea(
                                x=520, y=0, width=520, height=520
                            )
                        )
                    ]
                )

                line_bot_api.reply_message(event.reply_token, message)

                message_doc = {
                    'message' : text,
                    'name' : profile.display_name,
                    'user_id' : u.user_id
                }

                message_new(u.user_id,message_doc)
                

                

            elif text == "交易紀錄":
                docs = db.collection("transaction").where('customerID','==', u.user_id).order_by("date", direction=firestore.Query.DESCENDING).get()
                contents = []
                for i in docs:
                    t_doc = i.to_dict()
                    contents.append(historyServices_flex(t_doc['customerNAME'], str(t_doc['date']).split(" ")[0],t_doc['product']))

                if len(contents) == 0:
                    reply_text = "您目前沒有交易紀錄呦"

                    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                        message = TextSendMessage(reply_text)
                        line_bot_api.reply_message(event.reply_token, message)
                else:   
                    carousel_contents = {
                        "type": "carousel",
                        "contents": contents}
                    line_bot_api.reply_message(event.reply_token, line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage('交易紀錄', carousel_contents)
                        )
                    )
            elif text == "投資風險屬性分析問卷":
                u.state = states.QUSTION.value
                doc["state"] = u.state

                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='一、請問您投資金融商品最主要的考量因素為何？(投資目的)',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                
                                action = PostbackAction(
                                            label='保持資產的流動性',
                                            display_text='保持資產的流動性',
                                            data='a'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='保本',
                                            display_text='保本',
                                            data='b'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='賺取固定的利息收益',
                                            display_text='賺取固定的利息收益',
                                            data='c'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='賺取資本利得(價差)',
                                            display_text='賺取資本利得(價差)',
                                            data='d'
                                        )
                            ),
                            QuickReplyButton(
                                action = PostbackAction(
                                            label='追求總投資報酬最大',
                                            display_text='追求總投資報酬最大',
                                            data='e'
                                        )
                            )
                        ])))
                u.quastionCount += 1
                doc["quastionCount"] = u.quastionCount
            elif text == '一顆星':
                div_doc = db.collection('sales').document(u.div_id).get().to_dict()
                div_doc["score"] += 1
                div_doc["serviceCount"] += 1
                db.collection("sales").document(u.div_id).update(div_doc)
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方給您一顆星的評價",
                        )
                    )
            elif text == '二顆星':
                div_doc = db.collection('sales').document(u.div_id).get().to_dict()
                div_doc["score"] += 2
                div_doc["serviceCount"] += 1
                db.collection("sales").document(u.div_id).update(div_doc)
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方給您二顆星的評價",
                        )
                    )
            elif text == '三顆星':
                div_doc = db.collection('sales').document(u.div_id).get().to_dict()
                div_doc["score"] += 3
                div_doc["serviceCount"] += 1
                db.collection("sales").document(u.div_id).update(div_doc)
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方給您三顆星的評價",
                        )
                    )
            elif text == '四顆星':
                div_doc = db.collection('sales').document(u.div_id).get().to_dict()
                div_doc["score"] += 4
                div_doc["serviceCount"] += 1
                db.collection("sales").document(u.div_id).update(div_doc)
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方給您四顆星的評價",
                        )
                    )
            elif text == '五顆星':
                div_doc = db.collection('sales').document(u.div_id).get().to_dict()
                div_doc["score"] += 5
                div_doc["serviceCount"] += 1
                db.collection("sales").document(u.div_id).update(div_doc)
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方給您五顆星的評價",
                        )
                    )
            else:

                ##reply_text = "Hi\n我是智能金融導購平台💼\n"
                # # reply_text += "有任何金融相關的問題都可以詢問我喔！\n"
                # # reply_text += "我會幫你轉接專業證券營業員與保險業務員\n"
                # # reply_text += "他們能幫你做詳細的介紹與申購👍"
                contents = welcome_flex()
                if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage('交易紀錄', contents)
                    )
                    


        elif u.state == states.QUSTION.value:
            reply_text = "問卷還未完成喔~"        
            message = TextSendMessage(reply_text)
            line_bot_api.reply_message(event.reply_token, message)
            u.state = states.START.value
            doc["state"] = u.state
            u.score = 0
            doc["score"] = u.score
            u.quastionCount = 0
            doc['quastionCount'] = u.quastionCount

        elif u.state == states.DIV.value:
            if text == "離開":
                reply_text = "您已離開對話"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
                line_bot_api.push_message(
                u.user_id,
                TextSendMessage(
                    text='請為剛才的服務評分',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action = MessageAction(label="一顆星", text="一顆星")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="二顆星", text="二顆星")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="三顆星", text="三顆星")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="四顆星", text="四顆星")
                            ),
                            QuickReplyButton(
                                action = MessageAction(label="五顆星", text="五顆星")
                            )
                        ])))
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方已離開對話",
                        )
                    )
                div_doc = UserData_get(u.div_id)
                div_u = toUser(div_doc)
                div_u.state = states.LOGIN.value
                div_doc["state"] = div_u.state
                UserData_update(div_u,div_doc)
                u.state = states.START.value
                doc["state"] = u.state
            else:
                line_bot_api.push_message(u.div_id, TextSendMessage(text=text))
        elif u.state == states.PETSQUSTION.value:
            if text == 'male' or text == 'female' :
                message = ImagemapSendMessage(
                    base_url='https://i.imgur.com/5YHMcSp.png',
                    alt_text='breed',
                    base_size=BaseSize(height=1674, width=1040),
                    actions=[
                        MessageImagemapAction(
                            text='貴賓狗',
                            area=ImagemapArea(
                                x=0, y=124, width=360, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='黃金獵犬',
                            area=ImagemapArea(
                                x=360, y=124, width=320, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='鬆獅狗',
                            area=ImagemapArea(
                                x=680, y=124, width=360, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='柯基',
                            area=ImagemapArea(
                                x=0, y=511, width=360, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='柴犬',
                            area=ImagemapArea(
                                x=360, y=511, width=320, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='馬爾濟斯',
                            area=ImagemapArea(
                                x=680, y=511, width=360, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='比熊犬',
                            area=ImagemapArea(
                                x=0, y=898, width=360, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='吉娃娃',
                            area=ImagemapArea(
                                x=360, y=898, width=320, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='米克斯',
                            area=ImagemapArea(
                                x=680, y=898, width=360, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='博美',
                            area=ImagemapArea(
                                x=0, y=1285, width=360, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='法鬥',
                            area=ImagemapArea(
                                x=360, y=1285, width=320, height=387
                            )
                        ),
                        MessageImagemapAction(
                            text='其他',
                            area=ImagemapArea(
                                x=680, y=1285, width=360, height=387
                            )
                        )
                    ]
                )

                line_bot_api.reply_message(event.reply_token, message)

            else:
                reply_text = "以下為我為您整理的寵物險資訊，供您參考😀"
                line_bot_api.push_message(
                        event.source.user_id,
                        TextMessage(
                            text=reply_text,
                        )
                    )                
                u.state = states.START.value
                doc["state"] = u.state

                carousel_template_message = TemplateSendMessage(
                    alt_text='保險方案',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/Tpuig6m.png',
                                action=URITemplateAction(
                                    label='點選看更多',
                                    uri='https://www.fubon.com/insurance/b2c/content/prod_pet/index.html#a'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/eRiEesM.png',
                                action=URITemplateAction(
                                    label='點選看更多',
                                    uri='https://www.sk858.com.tw/products/pl/pet-insurance?utm_source=google&utm_medium=cpc&utm_campaign=petrespon&gclid=CjwKCAjwydP5BRBREiwA-qrCGrcxIm3YfdQmIh2h1zv4C5PyW72vqdrZdbFVDOllrUu7cBYXrzBayRoCtH8QAvD_BwE'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/kkKAxiT.png',
                                action=URITemplateAction(
                                    label='點選看更多',
                                    uri='https://www.cathay-ins.com.tw/INSEBWeb/BOBE/pet/pet_quote/prompt?projectId=Q1VTMDAwMw%3D%3D&utm_source=google&utm_medium=cpc&utm_campaign=A_08_搜尋_品牌字(寵物險)_品牌字&gclid=CjwKCAjwydP5BRBREiwA-qrCGs9UZbSSfuQ0Ch_ov4HzIA1J3wd5--aYadNHVvnMtQrD5ME7DKS-rRoCAEwQAvD_BwE'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/iw2jome.png',
                                action=URITemplateAction(
                                    label='點選看更多',
                                    uri='https://www.msig-mingtai.com.tw/MobileWeb/Pet/Insure/Index'
                                )
                            )                                                        
                        ]
                    )
                )
                line_bot_api.push_message(event.source.user_id, carousel_template_message)

                reply_text = "我已幫您找到了幾個保險業務員，您可以更深入的向他們詢問相關問題😉"
                line_bot_api.push_message(
                        event.source.user_id,
                        TextMessage(
                            text=reply_text,
                        )
                    )
                carousel_template_message = TemplateSendMessage(
                    alt_text='保險業務員',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/Hz8f9N3.jpg',
                                title='👔保險業務員 嘉禾',
                                text='您好，我是嘉禾，擔任保險業務員已有10年經歷，希望能用我的專業為您服務 !😁',
                                actions=[
                                    PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentjerry'
                                        ),
                                    PostbackTemplateAction(
                                        label = '諮詢',
                                        data='jerry'
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/n06HVkC.jpg',
                                title='👔保險業務員 麥基',
                                text='您好，我是麥基，有8年保險業資歷，很高興能為您服務。👍',
                                actions=[
                                    PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentmaggie'
                                        ),
                                    PostbackTemplateAction(
                                        label = '諮詢',
                                        data='maggie'
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/pDtoSWN.jpg',
                                title='👔保險業務員 曉琪',
                                text='您好，我是曉琪，我在保險業界服務5年了喔，很高興能為您服務!😉',
                                actions=[
                                    PostbackTemplateAction(
                                            label='查看評價', 
                                            data='commentapple'
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


    else:
        if u.state == states.START.value:

            reply_text = "請輸入【手機號碼】登入系統"

            
            message = TextSendMessage(reply_text)
            line_bot_api.reply_message(event.reply_token, message)
            u.state = states.UNLOGIN.value
            doc["state"] = u.state
        elif u.state == states.UNLOGIN.value:
            if text == '4wyd':
                reply_text = "歡迎登入\n請點選下方【服務項目】執行動作"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
                u.state = states.LOGIN.value
                doc["state"] = u.state
                headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json","Content-Type":"application/json"}

                req = requests.request('POST', ' https://api.line.me/v2/bot/user/' + u.user_id + '/richmenu/' + 'richmenu-9a3e9e8fd2ca493c4b6c1c638ea5304d', 
                       headers=headers)
                UserData_update(u,doc)

            if(text == "確認"): 
                reply_text = "輸入【簡訊驗證碼】登入系統"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            elif(text == "修改"):
                reply_text = "輸入【手機號碼】登入系統"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                carousel_template_message = TemplateSendMessage(
                    alt_text="請確認手機號碼是否正確：",
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://i.imgur.com/KH8be5G.jpg',
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
        
        elif u.state == states.LOGIN.value:
            if text == "登出":
                reply_text = "您已成功登出"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
                
                u.state = states.START.value
                doc["state"] = u.state
                headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json","Content-Type":"application/json"}
                req = requests.request('POST', ' https://api.line.me/v2/bot/user/' + u.user_id + '/richmenu/' + 'richmenu-79d96cd20dc3c93d4f4e69911d0118a4', 
                        headers=headers)

            elif text == "業績英雄榜":
                contents = rank_flex()
                line_bot_api.reply_message(event.reply_token, line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage('交易紀錄', contents)
                    )
                )
            elif text == "歷史服務紀錄":
                docs = db.collection("transaction").where('salesID','==', u.user_id).order_by("date", direction=firestore.Query.DESCENDING).get()
                contents = []
                for i in docs:
                    t_doc = i.to_dict()
                    contents.append(historyServices_flex(t_doc['customerNAME'], str(t_doc['date']).split(" ")[0],t_doc['product']))

                if len(contents) == 0:
                    reply_text = "您目前沒有交易紀錄呦"
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                else:   
                    carousel_contents = {
                        "type": "carousel",
                        "contents": contents}
                    line_bot_api.reply_message(event.reply_token, line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage('交易紀錄', carousel_contents)
                        )
                    )
            elif text == "本月分潤獎金":
                s_doc = db.collection('sales').document(u.user_id).get()
                reply_text = "您的本月分潤獎金為\n【" + str(s_doc.to_dict()['profit'])  +  "】元"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)

            elif text == "導購諮詢連結":
                
                docs = db.collection('message').where('sales_id','==', u.user_id).get()
                columns = []
                if len(list(db.collection('message').list_documents())) == 0:
                    
                    reply_text = "目前沒有導購諮詢呦"
                    message = TextSendMessage(reply_text)
                    line_bot_api.reply_message(event.reply_token, message)
                else:
                    for i in docs:
                        m_doc = i.to_dict()
                        columns.append(
                            CarouselColumn(
                                thumbnail_image_url= line_bot_api.get_profile(m_doc['user_id']).picture_url,
                                title=m_doc['name'],
                                text=m_doc['message'],
                                actions=[
                                    PostbackTemplateAction(
                                        label='接受諮詢', 
                                        data=m_doc['user_id']
                                    )
                                ]
                            )
                        )
                    
                    carousel_template_message = TemplateSendMessage(
                        alt_text='保險產品',
                        template=CarouselTemplate(
                            columns
                        )
                    )
                    line_bot_api.reply_message(event.reply_token, carousel_template_message)

        elif u.state == states.DIV.value :
            if text == "離開":
                reply_text = "您已離開對話"
                message = TextSendMessage(reply_text)
                line_bot_api.reply_message(event.reply_token, message)
                line_bot_api.push_message(
                        u.div_id,
                        TextMessage(
                            text="對方已離開對話",
                        )
                    )
                
                div_doc = UserData_get(u.div_id)
                div_u = toUser(div_doc)
                div_u.state = states.START.value
                div_doc["state"] = div_u.state
                UserData_update(div_u,div_doc)

                u.state = states.LOGIN.value
                doc["state"] = u.state
            else:

                if (u.div_id != 0):
                    line_bot_api.push_message(
                            u.div_id,
                            TextMessage(
                                text=text,
                            )
                        )

    UserData_update(u,doc)

    
    

    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    