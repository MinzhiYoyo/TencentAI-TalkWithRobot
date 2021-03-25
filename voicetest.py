import cv2
import voice_text

id = 2159946356
key = 'V5UoIbRZGBF9CNJ1'

format = 2
volume = 0

speaker = 6-5
speed = 100 - 50
aht = 0 + 24
apc = 58

v = voice_text.voice_text(id, key)

def play():
	v.text_to_voice("欧尼酱，欧嗨哟！", speaker + 5  ,  2 ,  0,  100 + 50 , aht - 24 , apc )
	v.text_to_voice("欧尼酱，欧嗨哟！", speaker + 5  ,  2 ,  0,  100 + 50 , aht - 24 , apc)
	# v.text_to_voice("欧尼酱，欧嗨哟！", speaker + 5  ,  2 ,  0,  100 + 50 , aht - 24 , apc)
	# v.text_to_voice("欧尼酱，欧嗨哟！", speaker + 5  ,  2 ,  0,  100 + 50 , aht - 24 , apc)
	# v.text_to_voice("欧尼酱，欧嗨哟！", speaker + 5  ,  2 ,  0,  100 + 50 , aht - 24 , apc)

def updata_speaker(value):
	global speaker
	speaker = value
	play()
def updata_speed(value):
	global speed
	speed = value
	play()
def updata_aht(value):
	global aht
	aht = value
	play()
def updata_apc(value):
	global apc
	apc = value
	play()
def main():
	cv2.namedWindow('voice')
	cv2.createTrackbar('speeker','voice', speaker, 2, updata_speaker )
	cv2.createTrackbar('speed','voice',speed ,150, updata_speed )
	cv2.createTrackbar('aht','voice', aht, 48, updata_aht )
	cv2.createTrackbar('apc','voice',apc , 100 , updata_apc )
	print('start playing')
	v.text_to_voice("欧尼酱，欧嗨哟！",filepath = 'hello')
	v.text_to_voice("欧尼酱，欧嗨哟！")
	cv2.waitKey(0)

if __name__ == '__main__':
	main()
