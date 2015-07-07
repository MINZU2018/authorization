# -*- coding: utf-8 -*-

import requests
import json

APPID = "wxafac6b4bc457eb26"
APPSECRET = "1a0c74ca64b2c33fe0eaefda149e293e"
PAYLOAD = {
	"grant_type": "client_credential",
	"appid": APPID,
	"secret": APPSECRET
}
URL = "https://api.weixin.qq.com/cgi-bin/token"


def get_access_token():
	response = requests.get(url=URL, params=PAYLOAD).content
	response = json.loads(response)
	if response["access_token"]:
	 	return response["access_token"]
	else:
		return response[errmsg]

# test
if __name__ == "__main__":
	print get_access_token()