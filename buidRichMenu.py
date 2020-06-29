import requests
import json

headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "服務項目",
    "chatBarText": "服務項目",
    "areas":[
        {
          "bounds": {"x": 551, "y": 325, "width": 321, "height": 321},
          "action": {"type": "message", "text": "up"}
        },
        {
          "bounds": {"x": 876, "y": 651, "width": 321, "height": 321},
          "action": {"type": "message", "text": "right"}
        },
        {
          "bounds": {"x": 551, "y": 972, "width": 321, "height": 321},
          "action": {"type": "message", "text": "down"}
        },
        {
          "bounds": {"x": 225, "y": 651, "width": 321, "height": 321},
          "action": {"type": "message", "text": "left"}
        },
        {
          "bounds": {"x": 1433, "y": 657, "width": 367, "height": 367},
          "action": {"type": "message", "text": "btn b"}
        },
        {
          "bounds": {"x": 1907, "y": 657, "width": 367, "height": 367},
          "action": {"type": "message", "text": "btn a"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)

from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=')

with open("clinet.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-9840c303b6ae2c0788e3973051045516", "image/jpeg", f)

import requests

headers = {"Authorization":"Bearer l82Nfs2Ji9XdgljwOFqOvPFQfQCytjakXuH1R8GB5oncFlzOPehHqxoj4utnElFJJBKfw2SUt2n7SiX56GIeSJwGglKRr0iCv78QttD7IaXe0zwxt9evRrbHObpOEp8FYCyTmqagFJt651108NGjYQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json","Content-Type":"application/json"}

req = requests.request('POST', ' https://api.line.me/v2/bot/user/all/richmenu/richmenu-9840c303b6ae2c0788e3973051045516', 
                       headers=headers)

print(req.text)
