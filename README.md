# TencentAI-TalkWithRobot
基于腾讯ai接口的语音闲聊，目前实现了语音转文字，闲聊回复，文字转语音并播放

## 基本函数（接口必需的信息）

### 1、生成sign签名

```python
	# 生成sign接口信息，对任意ai都通用，接口鉴权
    # APPKEY:换成你的app_APPKEY
	def get_sign(self,data):
		lst = [i[0]+'='+parse.quote_plus(str(i[1])) for i in data.items()]
		params = '&'.join(sorted(lst))
		s = params + '&app_key=' + APPKEY
		#print(s)
		h = hashlib.md5(s.encode('utf8'))
		return h.hexdigest().upper()
```



### 2、生成time_stamp

```python
	# 生成time_stamp，对任意ai都通用
	def get_time_stamp(self):
		return (int)(time.time())
```

### 3、生成nonce_str

```python
	# 生成nonce_str的
	def get_nonce_str(self):
		nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
		return nonce_str
```

## 语音转文本

更多参看请看：https://ai.qq.com/doc/aaiasr.shtml

```python
import requests as rq # 发送post请求
import base64 # 编码与解码
import time
import pyaudio # 为了录音
import wave # 为了录音
# 最大录音时间为15秒 这个函数是为了录音 函数源码请自行下载
def recording(self, record_time = 15)

# 进行编码操作
def ToBase64(self, file, debug = False)

# 参数说明：
#	speech: 语音数据的base64码
#	format: 1-->PCM 2-->WAV 3-->AMR 4-->SILK
#	rate: 采样频率： 8000-->8khz 16000-->16khz
# 返回值：
#	返回响应数据的json格式，需要的内容是['data']['text']，是string类型数据
def voice_to_text(speech , format = 2, rate = 16000, debug = False):
    	# 生成基本请求数据
		url_request = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr'
		time_stamp = get_time_stamp()
		nonce_str = get_nonce_str()
		data = {
			'app_id': 你的id
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
		header['Content-Type'] = 'application/x-www-form-urlencoded' # 没有这个header会报错的
		if debug :
			print('voice_to_text request data:',data)
		r = rq.post(url_request,headers = header,data = data)
		answer = r.json()
		return answer

```

## 闲聊

更多参看请看：https://ai.qq.com/doc/nlpchat.shtml

```python
# session 要保证是这个应用中唯一的标识，上限为32字节
def chat(self,question, session = '10000', debug = False):
		nonce_str = get_nonce_str()
		time_stamp = get_time_stamp()
		data = {
			'app_id' : 你的id,
			'time_stamp': time_stamp,
			'session' : session,
			'question': question,
			'nonce_str':nonce_str
		}
		data['sign'] = get_sign(data)
		r = rq.post('https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat',data = data)
        answer = r.json()
		return answer

```

## 文本转语音

更多参看请看：https://ai.qq.com/doc/aaitts.shtml

```python
# 参数说明
#	text: 需要转换的文字
#	speaker: 语音发音人编码 1--> 普通话男生; 5-->静琪女声 ; 6-->欢馨女声 ; 7-->碧萱女声
#	format:编码格式 1-->PCM ; 2-->WAV ;3-->MP3
#	volume: 声音音量：[-10,10],0为默认音量
#	speed: 合成语音速度[50,200]，默认100
#	aht: 音高[-24,24]
#	apc:音色，即频谱翘曲程度[0,100]
#	url:
# 返回值：返回响应数据的json格式 需要的内容是['data']['speech']，是base64编码数据
	def text_to_voice(self,text, speaker = 6 , format = 2 , volume = 0, speed = 100 , aht = 0 , apc = 58 , url = 'lab'):
		url_request = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tts'
		# 替换掉字符~，不然输出的时候出bug
		text.replace('~',',')
        # 生成基本签名信息
		time_stamp = get_time_stamp()
		nonce_str = get_nonce_str()
		
		tuozhan = '.mp3'
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
		# print(data)
		# header需要加这个参数，不然会报4096错误
		# 这个官方文档写的需要get，但是实际上是post才行
		r = rq.post(url_request,headers = header,data = data)
		answer = r.json()

        # 以时间来命名
		localtime = time.localtime(time.time())
		filename = './' + str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3]) + str(localtime[4]) + str(localtime[5])
        # ToFile函数在下面，请往下参看
		ToFile( answer['data']['speech'] , filename + tuozhan )
		playsound(filename + tuozhan)
		return answer  
```

```python
# 将base64（data）解码之后保存在fileName中
# 函数比较简单，一看就能知道
	def ToFile(self, data, fileName):
		# with open(txt, 'r') as fileObj:
		# 	base64_data = fileObj.read()
		ori_image_data = base64.b64decode(data)
		# print(ori_image_data)
		fout = open(fileName, 'wb')
		fout.write(ori_image_data)
		fout.close()
```



