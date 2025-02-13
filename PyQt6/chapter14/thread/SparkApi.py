#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SparkApi.py
@Time    :   2023/07/30 09:31:49
@Author  :   yangff 
@Version :   1.0
@微信公众号: 学点编程吧
'''
# 这部分代码有一部来源于科大讯飞的“星火认知大模型”提供的Python 调用示例

import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import logging
import os

# 加入日志
# 获取logger实例
logger = logging.getLogger("error")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s%(levelname)-8s:%(message)s')
current_dir = os.path.dirname(os.path.abspath(__file__)) # 当前目录
# 文件日志
file_handler = logging.FileHandler(f"{current_dir}\\error.log", encoding='utf-8')

file_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)

logger.setLevel(logging.INFO)

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

# 收到websocket错误的处理
def on_error(ws, error):
    logger.error(f"存在错误：{error}")

def error(code, data):
    logger.error(f"错误代码：{code}，内容：{data}")


# 收到websocket关闭的处理
def on_close(*ws):
    logger.info(f"连接关闭")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))

def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, question=ws.question))
    ws.send(data)

def gen_params(appid, question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": "general",
                "random_threshold": 0.5,
                "max_tokens": 2048,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": [
                    {"role": "user", "content": question}
                ]
            }
        }
    }
    return data