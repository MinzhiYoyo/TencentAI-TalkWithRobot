# 一、网站

[腾讯AI官网](https://ai.qq.com/)

# 二、概述

使用方法：

```
首先，自行申请应用：https://ai.qq.com/console/application/create-app

然后，获取APPID，APPKEY

生成 Json 请求数据

将请求数据提交给对应API接口

解析响应数据
```

# 三、基础函数

因为很多接口的请求数据都有重复的且通用的，所以用下面代码生成公共接口数据

```python
from urllib import parse
import hashlib
import requests as rq
import time
import random
import string

APPID = 1xxxxxxxx # 输入自己的app_id
APPKEY = 'Vxxxxxxxxxx' # 输入自己的app_key

# 下列函数参考于别的网址，侵权删

# 生成sign接口信息，接口鉴权
def get_sign(self,data):
	lst = [i[0]+'='+parse.quote_plus(str(i[1])) for i in data.items()]
	params = '&'.join(sorted(lst))
	s = params + '&app_key=' + self.APPKEY
	#print(s)
	h = hashlib.md5(s.encode('utf8'))
	return h.hexdigest().upper()

# 生成time_stamp
def get_time_stamp(self):
	return (int)(time.time())

# 生成nonce_str的
def get_nonce_str(self):
	nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
	return nonce_str
```



# 四、接口学习

## 1、智能闲聊接口

[参考文档请点这](https://ai.qq.com/doc/nlpchat.shtml)

#### 示例程序（python）：

```python
def chat(question):
	# 下面两个函数请看上一章节
	nonce_str = get_nonce_str() 
	time_stamp = get_time_stamp()
    app_id = 1xxxxxxxxx # 你的app_id
    url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat' # api网址
    
    # 请求json数据
    data={
        'app_id' : app_id,
		'time_stamp': time_stamp,
		'session' : '10000',
		'question': question,
		'nonce_str':nonce_str
    }
    data['sign'] = get_sign(data) # 函数在上一章节，生成sign数据
    r = rq.post(url,data = data) # 发送post请求
    answer = r.json()['data']['answer'] # 响应数据的答案，可以自行打印一下json的数据来看看
    return answer 

```

## 2、语音合成接口（文字转语音

[参考网址请点这](https://ai.qq.com/doc/aaitts.shtml)

#### 示例程序（python）：

```python
from playsound import playsound
import base64
import time

def ToFile( data, fileName): # 将base64文件解密，然后保存在fileName的文件中
		ori_image_data = base64.b64decode(data)
		fout = open(fileName, 'wb')
		fout.write(ori_image_data)
		fout.close()

        
def text_to_voice(text, speaker = 6 , format = 2 , volume = 0, speed = 100 , aht = 0 , apc = 58 ):
		url_request = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tts' # 有两个api，我们用其中的一个
		# 替换掉以下字符，不然输出的时候出bug
		text.replace('~',',')
		text.replace('；','。')
		text.replace('“',',')
		text.replace('”',',')
        
		# 同上章节
		time_stamp = get_time_stamp()
		nonce_str = get_nonce_str()
        app_id = 1xxxxxxxxx # 你的app_id
        
		data = {
			'app_id':app_id,
			'time_stamp': time_stamp,
			'nonce_str': nonce_str, 
			'speaker': speaker, 
			'format': format, 
			'volume': volume, 
			'speed': speed, 
			'text': text, 
			'aht': aht, 
			'apc': apc
		}
		data['sign'] = self.inter.get_sign(data)
		header = {

		}
		header['Content-Type'] = 'application/x-www-form-urlencoded'
		# header需要加这个参数，不然会报4096错误
        
		# 这个官方文档写的需要get请求，但是实际上是post才行
		r = rq.post(url_request,headers = header,data = data)
		answer = r.json()
		
        # 生成文件名（以时间戳），因为返回的数据是音频，所以我们需要先保存在本地，然后进行播放
		localtime = time.localtime(time.time())
		filename = './' + str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3]) + str(localtime[4]) + str(localtime[5]) + '.wav'
        
        # 将base64编码保存为文件，前面提到的一个函数
		ToFile( answer['data']['speech'] , filename) 
		playsound(filename) # 这个是python第三方库
		# os.remove(filename + tuozhan) # 如果就在这里删除好像会报错
		return answer  # 返回响应json数据
```

## 3、语音识别接口（语音转文字

[参考网址请点这](https://ai.qq.com/doc/aaiasr.shtml)

#### 示例程序（python）：

```python
import time
import pyaudio
import wave
import base64

# 录音
# 需要额外安装python库
# 安装pyaudio库，这个有点困难，需要参看：https://zhuanlan.zhihu.com/p/62455580
def recording( record_time = 3 ): 
		CHUNK = 1024
		FORMAT = pyaudio.paInt16 # 设置格式
		CHANNELS = 1 # 设置通道数
		RATE = 16000 # 设定采样频率
		RECORD_SECONDS = record_time # 设定计时秒数
        
        # 时间戳保存文件，以wav格式
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
		wf.writeframes(b''.join(frames)) # 以bytes格式写入文件中
		wf.close()
		return filename # 返回保存的文件名

def ToBase64(file): # 将文件转成base64编码格式的字符串
	with open(file, 'rb') as fileObj:
		image_data = fileObj.read()
		base63_data = base64.b64encode(image_data)  
        
        # 没有这一句就会报16388错误，因为我们需要转换成字符串进行提交吧
		base64_data = base63_data.decode("utf-8")
        
		return base64_data # 返回base64编码数据，且是字符串形式

def voice_to_text( speech , format = 2, rate = 16000 ):
		url_request = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr' # 用的是短语音识别，不是流
        
        # 同上
		time_stamp = get_time_stamp()
		nonce_str = get_nonce_str()
        app_id = 1xxxxxxxxx # 你的app_id

		data = {
			'app_id': app_id,
			'time_stamp': time_stamp,
			'nonce_str': nonce_str, 
			'format': str((int)(format)), 
			'speech': speech,
			'rate': str((int)(rate))
		}
		data['sign'] = self.inter.get_sign(data)
		header = {

		}
		header['Content-Type'] = 'application/x-www-form-urlencoded'
		r = rq.post(url_request,headers = header,data = data)
		answer = r.json()
		return answer
```

# 结束语

相信学了这么多，应该多少对这个有点了解了吧，还有更多的Ai接口等待你们去玩。