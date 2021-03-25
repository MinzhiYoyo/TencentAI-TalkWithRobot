import BasicFunction
import requests as rq
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.parse import quote_plus
import base64
from playsound import playsound
import os
import time
import pyaudio
import wave
import Smart_Chat

# base64.b64encode(s) 编码
# base64.b64decode(s) 解码

class voice_text:
	def __init__(self, App_id, app_APPKEY ):
		self.inter = BasicFunction.basicInterface(App_id, app_APPKEY)
		self.url_Lab = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tts'
		self.url_youtu = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tta'
		self.url_voice_text = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr'
		self.format = 2
		self.chat = Smart_Chat.smartChat(App_id, app_APPKEY)


	def speek_with_robot(self, record_time = 3):
		while True:
			print('你有',record_time,'秒钟时间来与我交谈哦！')
			str = self.recording(record_time)
			base641 = self.ToBase64(str)
			question = self.voice_to_text(base641,debug = False)
			print('时间到---> ', question['data']['text'])
			if question['data']['text'] == '拜拜':
				test = '呜呜呜，拜拜啦，你要快点来找我玩哦，不然我会孤独的，哭哭'
				print(test)
				self.text_to_voice(test)
				break
			answer = self.chat.chat(question['data']['text'],debug = False )
			print('      ---> ',answer)
			self.text_to_voice(answer)

# 录音record_time秒钟并保存在以时间命名的文件里，是wav格式
# 返回录音的base64编码格式
	def recording(self, record_time = 15):
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 16000
		RECORD_SECONDS = record_time
		localtime = time.localtime(time.time())
		filename = './' + str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3]) + str(localtime[4]) + str(localtime[5])
		filename = filename + '.wav'
		WAVE_OUTPUT_FILENAME = filename
		p = pyaudio.PyAudio()
		stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
		frames = []
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)
		stream.stop_stream()
		stream.close()
		p.terminate()
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # 保存为文件
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		# wf.writeframes(str(frames))
		wf.close()
		return filename
# 参数说明：
#	speech: 语音数据的base64码
#	format: 1-->PCM 2-->WAV 3-->AMR 4-->SILK
#	rate: 采样频率： 8000-->8khz 16000-->16khz
# 返回值：
#	返回响应数据的json格式，需要的内容是['data']['text']，是string类型数据
	def voice_to_text(self, speech , format = 2, rate = 16000, debug = False):
		self.format = format
		url_request = self.url_voice_text
		time_stamp = self.inter.get_time_stamp()
		nonce_str = self.inter.get_nonce_str()
		if format != 1 or format != 2 or format!= 3 or format != 4:
			format = 2
		if rate != 8000 or rate != 16000:
			rate = 16000
		data = {
			'app_id': self.inter.app_id,
			'time_stamp': time_stamp,
			'nonce_str': nonce_str, 
			'format': str((int)(format)), 
			# 'speech': str(speech)[1:],
			'speech': speech,
			'rate': str((int)(rate))
		}
		data['sign'] = self.inter.get_sign(data)
		header = {

		}
		header['Content-Type'] = 'application/x-www-form-urlencoded'
		if debug :
			print('voice_to_text request data:',data)
		r = rq.post(url_request,headers = header,data = data)
		answer = r.json()
		if debug:
			print('voice_to_text response data:',answer)
		return answer
# 语音转文字
# 参数说明
#	text: 需要转换的文字
#	speaker: 语音发音人编码 1--> 普通话男生; 5-->静琪女声 ; 6-->欢馨女声 ; 7-->碧萱女声
#	format:编码格式 1-->PCM ; 2-->WAV ;3-->MP3
#	volume: 声音音量：[-10,10],0为默认音量
#	speed: 合成语音速度[50,200]，默认100
#	aht: 音高[-24,24]
#	apc:音色，即频谱翘曲程度[0,100]
#	url:
#	isplay: 是否直接播放
#	debug: 是否调试
# 返回值：返回响应数据的json格式 需要的内容是['data']['speech']，是base64编码数据
	def text_to_voice(self,text, speaker = 6 , format = 2 , volume = 0, speed = 100 , aht = 0 , apc = 58 , url = 'lab',isplay = True,debug = False,filepath = ''):
		url_request = self.url_Lab
		format = self.format
		# 替换掉字符~，不然输出的时候出bug
		text.replace('~',',')
		text.replace('；','。')
		text.replace('“',',')
		text.replace('”',',')
		if url == 'youtu':
			url_request = self.url_youtu
		time_stamp = self.inter.get_time_stamp()
		nonce_str = self.inter.get_nonce_str()
		# 对数据进行约束大小
		if speaker != 1 and speaker != 5 and speaker != 6 and speaker != 7:
			speaker = 6
		
		tuozhan = '.mp3'
		if format == 1:
			tuozhan = '.pcm'
		if format == 2:
			tuozhan = '.wav'
		
		if format != 1 and format != 2 and format != 3:
			format = 3

		if volume > 10:
			volume = 10
		if volume < -10:
			volume = -10

		if speed < 50:
			speed = 50
		if speed > 200:
			speed = 200

		if aht < -24:
			aht = 24
		if aht > 24:
			aht = 24

		if apc > 100:
			apc = 100
		if apc < 0:
			apc = 0
		# Get请求的数据
		# data = {
		# 	'app_id': self.inter.app_id,
		# 	'time_stamp': time_stamp,
		# 	'nonce_str': nonce_str, 
		# 	'speaker': (int)(speaker), 
		# 	'format': (int)(format), 
		# 	'volume': (int)(volume), 
		# 	'speed': (int)(speed), 
		# 	'text': text, 
		# 	'aht': (int)(aht), 
		# 	'apc': (int)(apc)
		# }
		data = {
			'app_id': self.inter.app_id,
			'time_stamp': time_stamp,
			'nonce_str': nonce_str, 
			# 'sign': '',
			'speaker': str((int)(speaker)), 
			'format': str((int)(format)), 
			'volume': str((int)(volume)), 
			'speed': str((int)(speed)), 
			'text': text, 
			'aht': str((int)(aht)), 
			'apc': str((int)(apc))
		}
		data['sign'] = self.inter.get_sign(data)
		header = {

		}
		header['Content-Type'] = 'application/x-www-form-urlencoded'
		if debug:
			print('test_to_voice request data:' , data)
		# print(data)
		# header需要加这个参数，不然会报4096错误
		# 这个官方文档写的需要get，但是实际上是post才行
		r = rq.post(url_request,headers = header,data = data)
		answer = r.json()
		if debug:
			print('test_to_voice response data:' , answer)
		
		localtime = time.localtime(time.time())
		filename = './' + str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3]) + str(localtime[4]) + str(localtime[5])
		if filepath:
			filename = filepath
		self.ToFile( answer['data']['speech'] , filename + tuozhan )
		if isplay:
			playsound(filename + tuozhan)
		# os.remove(filename + tuozhan)
		return answer  

# 将file里面的文件编码成base64并返回base64编码
	def ToBase64(self, file, debug = False):
		with open(file, 'rb') as fileObj:
			image_data = fileObj.read()
			base63_data = base64.b64encode(image_data)  
			base64_data = base63_data.decode("utf-8") # 没有这一句就会报16388错误
			if debug:
				print(file,' to base64:',base64_data)
			return base64_data
	
	# 将base64（data）解码之后保存在fileName中
	def ToFile(self, data, fileName):
		# with open(txt, 'r') as fileObj:
		# 	base64_data = fileObj.read()
		ori_image_data = base64.b64decode(data)
		# print(ori_image_data)
		fout = open(fileName, 'wb')
		fout.write(ori_image_data)
		fout.close()
 
# ToBase64("./desk.jpg",'desk_base64.txt')  # 文件转换为base64
# ToFile("./desk_base64.txt",'desk_cp_by_base64.jpg')  # base64编码转换为二进制文件

if __name__ == '__main__':
	v = voice_text(2159946356,'V5UoIbRZGBF9CNJ1')
	v.speek_with_robot()

	# v.ToFile('itiscool','./test.txt')
	# print(base64.b64decode(v.ToBase64('./test.txt')))

	# question = '梁炜是傻逼'
	# answ = v.text_to_voice(question,debug = True,isplay = True)
	# # print(answ)
	# print(v.voice_to_text(answ, debug = True))


