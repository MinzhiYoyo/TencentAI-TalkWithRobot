import BasicFunction
import requests as rq
import time

# 返回数据：json格式
# {
#   "ret": 0, # 0表示正确返回了，非0表示错误
#   "msg": "ok", # ret为0就是ok，非0返回错误原因
#   "data": {
#       "session": "10000", # 唯一标识
#       "answer": "我叫小豪豪~" # 回答 
#   }
# }


class smartChat:
	def __init__(self, App_id, app_APPKEY, defaultAnswer = '我也不知道该怎么回答了，嘤嘤嘤，要不你给我买糖糖吃'):
		self.inter = BasicFunction.basicInterface(App_id, app_APPKEY)
		self.url_chat = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
		self.DefaultAnswer = defaultAnswer

	# session 要保证是这个应用中唯一的标识，上限为32字节
	# 返回值：是string类型
	def chat(self,question, session = '10000', debug = False):
		nonce_str = self.inter.get_nonce_str()
		time_stamp = self.inter.get_time_stamp()
		data = {
			'app_id' : self.inter.app_id,
			'time_stamp': time_stamp,
			'session' : session,
			'question': question,
			'nonce_str':nonce_str
		}
		data['sign'] = self.inter.get_sign(data)
		if debug:
			print('chat request data:',data)
		r = rq.post(self.url_chat,data = data)
		answer = ''
		if debug:
			print('chat response data：',r.json())
		if r.json()['ret'] == 0:
			answer = r.json()['data']['answer']
			if debug:
				print('answer:',answer)
		elif r.json()['ret'] == 16394:
			answer = self.DefaultAnswer
			if debug:
				print('defaule answer:',answer)
		else :
			answer = r.json()['msg']
			if debug:
				print('error msg:',answer)
		if answer:
			return answer
		else :
			return self.DefaultAnswer


		