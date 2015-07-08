# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import hashlib
from wechat_sdk import WechatBasic
import os.path
import requests
import json

import sys
sys.path.append("..")

from util.get_access import get_access_token

token = "token"
APPID = "appid"
APPSECRET = "appsecret"

class MainHandler(tornado.web.RequestHandler):

	def get(self):
		# signature = self.get_argument("signature", None)
		# timestamp = self.get_argument("timestamp", None)
		# nonce = self.get_argument("nonce", None)
		# echostr = self.get_argument("echostr", None)
		# lst = [timestamp, nonce, token]
		# lst.sort()
		# sha1 = hashlib.sha1()
		# map(sha1.update, lst)
		# hashcode=sha1.hexdigest()
		# if hashcode == signature:
		# 	self.write(echostr)
		pass
      

	def post(self):
		# 实例化 wechat
		wechat = WechatBasic(token=token)
		signature = self.get_argument("signature", None)
		timestamp = self.get_argument("timestamp", None)
		nonce = self.get_argument("nonce", None)
        # 对签名进行校验
		if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
		    # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
		    # look request method
			# print dir(self.request)
		    content = self.request.body
		    wechat.parse_data(content)
		    # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
		    message = wechat.get_message()

		    response = None
		    if message.type == 'text':
		        if message.content == 'wechat':
		        	response = wechat.response_text(u'''
		        		<a href="https://open.weixin.qq.com/connect/oauth2/authorize?
		        		appid=wxafac6b4bc457eb26&redirect_uri=http://tuteng.info/login_access&
		        		response_type=code&scope=snsapi_userinfo&state=14#wechat_redirect">testtt</a>
		        		''')
		        else:
		            response = wechat.response_text(u'world')
		    elif message.type == 'image':
		        response = wechat.response_text(u'image')
		    else:
		        response = wechat.response_text(u'no image')
		   	# print response
			# 此处出现问题，一直干扰获取授权，导致code得不到，access_token,出错
		    #self.write(response)


class LoginAccess(tornado.web.RequestHandler):

	def get(self):
		code = self.get_argument("code", None)
		print code
		get_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
		token_payload = {
			"appid": APPID,
			"secret": APPSECRET,
			"code": code,
			"grant_type": "authorization_code"
		}
		response = requests.get(url=get_token_url, params=token_payload).content
		print response
		response = json.loads(response)
		get_info_url = "https://api.weixin.qq.com/sns/userinfo"
		print response["access_token"]
		info_payload = {
			"access_token": response["access_token"],
			"openid": response["openid"],
			"lang": "zh_CN"
		}
		info_response = requests.get(url=get_info_url, params=info_payload).content
		info_response = json.loads(info_response)
		self.render(
			"get_access.html",
			province=info_response["province"],
			openid=info_response["openid"],
			city=info_response["city"],
			sex=1,
			headimgurl=info_response["headimgurl"],
			language=info_response["language"],
			nickname=info_response["nickname"],
			country=info_response["country"]
			)

	def post(self):
		pass


application = tornado.web.Application([
    (r"/", MainHandler),
#    (r"/login_access", LoginAccess),
    ],
   template_path=os.path.join(os.path.dirname(__file__), "templates"),
   static_path=os.path.join(os.path.dirname(__file__), "static"),
)
# 省去配置nginx，方便测试
application.add_handlers(r"^tuteng.info$",[
		(r"/login_access", LoginAccess),
	])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
