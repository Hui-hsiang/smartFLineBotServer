#%%
import requests
import json

headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

body = {
    "size": {"width": 1200, "height": 810},
    "selected": "true",
    "name": "點選此處以使用功能",
    "chatBarText": "點選此處以使用功能",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 400, "height": 405},
          "action": {"type": "message", "text": "交易紀錄"}
        },
        {
          "bounds": {"x": 400, "y": 0, "width": 400, "height": 405},
          "action": {"type": "message", "text": "保險產品"}
        },
        {
          "bounds": {"x": 800, "y": 0, "width": 400, "height": 405},
          "action": {"type": "message", "text": "保險小知識"}
        },
        {
          "bounds": {"x": 0, "y": 405, "width": 400, "height": 405},
          "action": {"type": "message", "text": "平台介紹"}
        },
        {
          "bounds": {"x": 400, "y": 405, "width": 400, "height": 405},
          "action": {"type": "message", "text": "最新活動"}
        },
        {
          "bounds": {"x": 800, "y": 405, "width": 400, "height": 405},
          "action": {"type": "message", "text": "常見問題"}
        }
    ]
  }

# body = {
#     "size": {"width": 2500, "height": 843},
#     "selected": "true",
#     "name": "服務項目",
#     "chatBarText": "服務項目",
#     "areas":[
#         {
#           "bounds": {"x": 0, "y": 0, "width": 625, "height": 843},
#           "action": {"type": "message", "text": "導購諮詢連結"}
#         },
#         {
#           "bounds": {"x": 625, "y": 0, "width": 625, "height": 843},
#           "action": {"type": "message", "text": "歷史服務紀錄"}
#         },
#         {
#           "bounds": {"x": 1250, "y": 0, "width": 625, "height": 843},
#           "action": {"type": "message", "text": "本月分潤獎金"}
#         },
#         {
#           "bounds": {"x": 1875, "y": 0, "width": 625, "height": 843},
#           "action": {"type": "message", "text": "業績英雄榜"}
#         }
#     ]
#   }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                        headers=headers,data=json.dumps(body).encode('utf-8'))

req_data = req.json()

print(req_data['richMenuId'])
id = req_data['richMenuId']
#%%
from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=')

with open("Client.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(id, "image/png", f)

import requests

headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json","Content-Type":"application/json"}

req = requests.request('POST', ' https://api.line.me/v2/bot/user/all/richmenu/richmenu-79d96cd20dc3c93d4f4e69911d0118a4', 
                       headers=headers)

print(req.text)


# %%
headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json","Content-Type":"application/json"}
req = requests.request('POST', ' https://api.line.me/v2/bot/user/' + 'U2649922b5604a80e08b0f9dba91f9029' + '/richmenu/' + 'richmenu-79d96cd20dc3c93d4f4e69911d0118a4', 
                        headers=headers)

# %%
