from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import os
import random
import sys
sys.path.append('/Users/takumito0604/python/LINE_BOT/LINE/bot')
from greeting_mes import aisatsu_mes
# Create your views here.

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.getenv("access_token")
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {ACCESS_TOKEN}"
}


def index(request):
    return HttpResponse("This is bot api.")


def reply_text(reply_token, text):
    reply=random.choice(aisatsu_mes)
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }
    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
    return reply

def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    return HttpResponse(reply)  # テスト用
