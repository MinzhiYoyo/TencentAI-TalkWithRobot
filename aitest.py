import voice_text
import Smart_Chat

id = 2111111111
key = 'Vxxxxxxxxxxx'

def main():
	v = voice_text.voice_text(id, key)
	c = Smart_Chat.smartChat(id, key)
	while True:
		q = input('输入end退出>')
		if q == 'end'  or q == '拜拜' or q == 'bye' or q == 'Bye' :
			print('嘤嘤嘤，拜拜啦，你要快点来找我玩哦，不然我会孤独的，哭哭')
			v.text_to_voice('嘤嘤嘤，拜拜啦，你要快点来找我玩哦，不然我会孤独的，哭哭')
			break
		a = c.chat(q)
		print('< ',a)
		if a:
			v.text_to_voice(a)
def talkWithRobot():
	v = voice_text.voice_text(2111111,'Vxxxxxxx')
	v.speek_with_robot()
if __name__ == '__main__':
	# main() # 打字进行交流
	talkWithRobot() # 语音聊天交流

