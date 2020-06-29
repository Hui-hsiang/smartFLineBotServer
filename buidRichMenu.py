# import requests
# import json

# headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

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

# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
#                         headers=headers,data=json.dumps(body).encode('utf-8'))

# req_data = req.json()

# print(req_data['richMenuId'])
# id = req_data['richMenuId']
# from linebot import (
#     LineBotApi, WebhookHandler
# )

# line_bot_api = LineBotApi('l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=')

# with open("seller.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image(id, "image/png", f)

import requests

headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json","Content-Type":"application/json"}

req = requests.request('POST', ' https://api.line.me/v2/bot/user/all/richmenu/' + 'richmenu-6b8167a5a521e96c320ca94ad954e6c6', 
                       headers=headers)

print(req.text)
