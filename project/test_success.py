# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import hashlib
from wechat_sdk import WechatBasic
import os.path

import sys
sys.path.append("..")

from util.get_access import get_access_token

token = "wechat"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument("signature", None)
        timestamp = self.get_argument("timestamp", None)
        nonce = self.get_argument("nonce", None)
        echostr = self.get_argument("echostr", None)
        lst = [timestamp, nonce, token]
        lst.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, lst)
        hashcode=sha1.hexdigest()
        if hashcode == signature:
                return self.write(echostr)

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
		             response = wechat.response_news([
			            {
			                'title': u'mytitle',
			                'description': u'jstiaozhuan',
			                'url': u'http://104.236.134.217/login_access'
			            }
			          ])
		        else:
		            response = wechat.response_text(u'world')
		    elif message.type == 'image':
		        response = wechat.response_text(u'image')
		    else:
		        response = wechat.response_text(u'no image')
		    print response
		    self.write(response)


class LoginAccess(tornado.web.RequestHandler):
	def get(self):
		self.render("get_access.html")

	def post(self):
		pass


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login_access", LoginAccess),
    ],
   template_path=os.path.join(os.path.dirname(__file__), "templates"),
   static_path=os.path.join(os.path.dirname(__file__), "static"),
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
