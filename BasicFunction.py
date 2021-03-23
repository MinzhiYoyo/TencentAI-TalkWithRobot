from urllib import parse
import hashlib
import requests as rq
import time
import random
import string

# 这个文件是用来生成某些必须的请求参数的

class basicInterface:
	def __init__(self,App_id,app_APPKEY):
		self.app_id = App_id
		self.APPKEY = app_APPKEY
	# 生成sign接口信息，对任意ai都通用，接口鉴权
	def get_sign(self,data):
		lst = [i[0]+'='+parse.quote_plus(str(i[1])) for i in data.items()]
		params = '&'.join(sorted(lst))
		s = params + '&app_key=' + self.APPKEY
		#print(s)
		h = hashlib.md5(s.encode('utf8'))
		return h.hexdigest().upper()

	# 生成time_stamp，对任意ai都通用
	def get_time_stamp(self):
		return (int)(time.time())

	# 生成nonce_str的
	def get_nonce_str(self):
		nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
		return nonce_str



