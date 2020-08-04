# -*- coding:utf-8 -*-
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests

class DingDing(object):
    """
    使用钉钉机器人发送消息
    """
    def __init__(self, secret, url):
        """
        构造函数，里面有实例属性timestamp时间戳，secret，url，sign最终的签名
        :param secret: 钉钉提供的secret String
        :param url: 钉钉提供的url String
        """
        # 把timestamp+"\n"+密钥当做签名字符串，使用HmacSHA256算法计算签名，然后进行Base64 encode，最后再把签名参数再进行urlEncode，得到最终的签名（需要使用UTF-8字符集）
        self.timestamp = str(round(time.time() * 1000))
        self.secret = secret
        self.url = url
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    def send_text(self, content, atMobiles=[],isAtAll=False):
        """
        发送文本消息
        :param content: 文本内容，String
        :param atMobiles: 要@的手机号码，List
        :param isAtAll: 是否@全体成员，Boolean
        :return: response.text，请求返回对象text String
        """
        msg = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": atMobiles,
                "isAtAll": isAtAll
            }
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"},data=json.dumps(msg))
        return response.text

    def send_link(self,text,title,pic_url,msg_url):
        """
        发送链接（文本、标题、图片、消息url）link
        :param text: 文本 String
        :param title: 标题 String
        :param pic_url: 图片地址 String
        :param msg_url: 消息地址 String
        :return: response.text，请求返回对象text String
        """
        msg = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": pic_url,
                "messageUrl": msg_url
            }
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"}, data=json.dumps(msg))
        return response.text

    def send_md_string(self,title,md_text,atMobiles=[],isAtAll=False):
        """
        传入markdown字符串，发送markdown消息
        :param title: 标题 String
        :param md_text: md文本 String
        :param atMobiles: 要@的手机号码，List
        :param isAtAll: 是否@全体成员，Boolean
        :return: response.text，请求返回对象text String
        """
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": md_text
            },
            "at": {
                "atMobiles": atMobiles,
                "isAtAll": isAtAll
            }
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"}, data=json.dumps(msg))
        return response.text

    def send_md_file(self,title,md_file_path,atMobiles=[],isAtAll=False):
        """
        传入markdown文档文件路径，发送markdown消息
        :param title: 标题 String
        :param md_file_path: markdown文档文件路径 String
        :param atMobiles: 要@的手机号码 List
        :param isAtAll: 是否@全体成员 Boolean
        :return: response.text，请求返回对象text String
        """
        with open(md_file_path,'r') as f:
            text = f.read()
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": atMobiles,
                "isAtAll": isAtAll
            }
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"}, data=json.dumps(msg))
        return response.text

    def send_actionCard_all_jump(self,title,md_text,singleTitle,singleURL,btnOrientation="0"):
        """
        发送整体跳转ActionCard类型的消息
        :param title: 标题 String
        :param md_text: markdown文本 String
        :param singleTitle: 单个按钮的标题 String
        :param singleURL: 点击singleTitle按钮触发的URL String
        :param btnOrientation: 0-按钮竖直排列，1-按钮横向排列 String="0"|"1"
        :return: response.text，请求返回对象text String
        """
        msg = {
            "actionCard": {
                "title": title,
                "text": md_text,
                # btnOrientation String 0-按钮竖直排列，1-按钮横向排列
                "btnOrientation": btnOrientation,
                "singleTitle" : singleTitle,
                "singleURL" : singleURL
            },
            "msgtype": "actionCard"
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"}, data=json.dumps(msg))
        return response.text

    def send_actionCard_all_jump_file(self,title,md_file,singleTitle,singleURL,btnOrientation="0"):
        """
        发送整体跳转ActionCard类型的消息
        :param title: 标题 String
        :param md_file: markdown文本文件路径 String
        :param singleTitle: 单个按钮的标题 String
        :param singleURL: 点击singleTitle按钮触发的URL String
        :param btnOrientation: 0-按钮竖直排列，1-按钮横向排列，在这种类型的消息中一般设置没有什么用 String="0"|"1"
        :return: response.text，请求返回对象text String
        """
        with open(md_file,'r') as f:
            md_text = f.read()
        msg = {
            "actionCard": {
                "title": title,
                "text": md_text,
                # btnOrientation String 0-按钮竖直排列，1-按钮横向排列
                "btnOrientation": btnOrientation,
                "singleTitle": singleTitle,
                "singleURL": singleURL
            },
            "msgtype": "actionCard"
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"}, data=json.dumps(msg))
        return response.text

    def send_actionCard_one_jump(self,title,md_text,btnOrientation,**kwargs):
        """
        发送独立跳转ActionCard类型的消息
        :param title: 标题 String
        :param md_text: markdown文本 String
        :param btnOrientation: 0-按钮竖直排列，1-按钮横向排列 String="0"|"1"
        :param kwargs: {title1:actionUrl1,title2:actionUrl2,...} Dictionary
        :return: response.text，请求返回对象text String
        """
        btns = []
        for item in kwargs:
            btns.append({"title": item, "actionURL": kwargs[item]})
        msg = {
            "actionCard": {
                "title": title,
                "text": md_text,
                "btnOrientation": btnOrientation,
                "btns": btns
            },
            "msgtype": "actionCard"
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"}, data=json.dumps(msg))
        return response.text

    def send_actionCard_one_jump_file(self,title,md_file,btnOrientation,**kwargs):
        """
        发送独立跳转ActionCard类型的消息
        :param title: 标题 String
        :param md_file: markdown文本文档路径 String
        :param btnOrientation: 0-按钮竖直排列，1-按钮横向排列 String="0"|"1"
        :param kwargs: {title1:actionUrl1,title2:actionUrl2,...} Dictionary
        :return: response.text，请求返回对象text String
        """
        with open(md_file,'r') as f:
            md_text = f.read()
        btns = []
        for item in kwargs:
            btns.append({"title": item, "actionURL": kwargs[item]})
        msg = {
            "actionCard": {
                "title": title,
                "text": md_text,
                "btnOrientation": btnOrientation,
                "btns": btns
            },
            "msgtype": "actionCard"
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"}, data=json.dumps(msg))
        return response.text

    def send_feedCard(self,*args):
        """
        发送feedCard类型的消息
        :param args: [title1,messageURL1,picURL1,.....] List
        :return: response.text，请求返回对象text String
        """
        links = []
        for i in range(0,len(args),3):
            links.append({"title": args[i], "messageURL": args[i+1], "picURL": args[i+2]})
        msg = {
            "feedCard": {
                "links": links
            },
            "msgtype": "feedCard"
        }
        url = self.url + "&timestamp=" + self.timestamp + "&sign=" + self.sign
        response = requests.post(url=url, headers={"content-type": "application/json"}, data=json.dumps(msg))
        return response.text

