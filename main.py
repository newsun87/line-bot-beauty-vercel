from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup
#import matplotlib.pyplot as plt
import concurrent.futures
import random
import os
import time
import pyimgur

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *
import json, os, time, requests

def get_image_url_list():
  image1_url_list = []
  # 取出所有網頁連結並存成串列
  page_url_list = []
  for i in range(1, 23):
    page_url = f"https://www.ptt.cc/bbs/Beauty/search?page={i}&q=author%3AGentlemon"
    page_url_list.append(page_url)
  for page_url in page_url_list:
   web = requests.get(page_url, cookies={'over18':'1'})    # 傳送 Cookies 資訊後，抓取頁面內容
   soup = BeautifulSoup(web.text, "html.parser")   # 使用 BeautifulSoup 取得網頁結構
   title_list = soup.find_all('div', class_='title')    # 取得所有 img tag 的內容
   for title in title_list:
        a_tag = title.find('a')
        href = a_tag['href']
        image1_url_list.append(href)
  print(f"圖片網頁所有連結數目 {len(image1_url_list)} 位美女")
  return image1_url_list
  
def get_image_src(image_url): # 取得任意一張圖片網址
  web = requests.get(image_url, cookies={'over18':'1'}) # 傳送 Cookies 資訊後，抓取頁面內容
  soup = BeautifulSoup(web.text, "html.parser")   # 使用 BeautifulSoup 取得網頁結構
  imgs = soup.find_all('img')    # 取得所有 img tag 的內容
  name = 0
  image_src_list = []  # 根據爬取的資料，建立一個圖片名稱與網址的空串列
  for i in imgs:
    image_src_list.append(i['src']) # 圖片網址加入 image_list 串列
    name = name + 1        # 編號增加 1
  print(f"圖片共有 {name} 張 ")
  while True:
    random_image_src = random.choice(image_src_list)
    if random_image_src != image_src_list[-1]:
        break
  print(f"圖片網址：{random_image_src}")  
  return random_image_src

# 你的 LINE Channel access token'
access_token = 'fd+DgyZ0BubTcS9FGRKSY3EaayAzhtPFhboPptqLImJBHo2+lG+qCqP3voCzbSMtaJN/lXfZwZHkCNgYr0TnQDbovXt3EDeJ8yervSC8KN1vAamg30mHFPBJaTcotIyb2SXN7IOTy8UvMdw911SWKAdB04t89/1O/w1cDnyilFU='
# 你的 LINE Channel access token
channel_secret = '0b145f6b1cbdf143030a916e5914143d'
# Channel Access Token
line_bot_api = LineBotApi(access_token)
# Channel Secret
line_handler = WebhookHandler(channel_secret)

# 開啟檔案並以讀取模式讀取資料
with open('./image_url.txt', 'r') as f:
    lines = f.readlines()

# 移除每一行的換行符號並存入串列
image_url_list = [line.strip() for line in lines]
print(image_url_list, len(image_url_list))

app = Flask(__name__)
# 監聽所有來自 LINE Bot Channel 的 Post Request
@app.route("/")
def index():
    return "Hello World"
@app.route("/webhook", methods=['POST'])
def linebot():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # 取得傳來的訊息文字
    body = request.get_data(as_text=True)
    print(f"訊息內容 {body}")
    # 轉換訊息內容成 JSON 物件
    json_data = json.loads(body)
    # 驗證訊息正確性
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理 LINE Bot channel 傳來訊息
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  if event.message.text =='help':
    messages=TextSendMessage(text='請輸入"美女圖"')
    line_bot_api.reply_message(event.reply_token, messages)
    
  if event.message.text =='美女圖':
    random_element = random.choice(image_url_list) # 任意取出其中一個網頁
    slected_image_url_path = f"https://www.ptt.cc{random_element}" # 完整圖片網頁網址
    print(f"隨機取出的圖片網頁連結 {slected_image_url_path}")
    random_image_src = get_image_src(slected_image_url_path)    
    # 指定要上傳的檔案路徑
    messages=ImageSendMessage(
            original_content_url=random_image_src,
            preview_image_url=random_image_src
          )
    line_bot_api.reply_message(event.reply_token, messages)

if __name__ == "__main__":   
  app.run()
