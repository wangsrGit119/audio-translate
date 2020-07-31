from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib
# import keras
from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
import sys
from general_function.file_wav import *


datapath = './'
modelpath = 'model_speech/'
ms = ModelSpeech(datapath)
ms.LoadModel(modelpath + 'speech_model251_e_0_step_625000.model')

ml = ModelLanguage('model_language')
ml.LoadModel()

host = ('127.0.0.1', 8888)
class HttpServerWB(BaseHTTPRequestHandler):
	def setup(self):
		self.request.settimeout(10)
		BaseHTTPRequestHandler.setup(self)
	
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	def do_GET(self):
		print(self.path)
		# print(self.headers)
		# print(self.request)
		if self.path == '/index.html':
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			self.wfile.write(json.dumps({'result':'首页'}).encode())
		elif self.path == '/about':
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			self.wfile.write(json.dumps({'result':'王建龙'}).encode())
		else:
			file_name = './index.html'
			f = open(file_name,'rb')
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			self.wfile.write(json.dumps({'result':'404'}).encode())
	def do_POST(self):  
		'''
		处理通过POST方式传递过来并接收的语音数据
		通过语音模型和语言模型计算得到语音识别结果并返回
		'''
		path = self.path  
		print(path)
		#获取post提交的数据  
		datas = self.rfile.read(int(self.headers['content-length']))  
		#datas = urllib.unquote(datas).decode("utf-8", 'ignore') 
		datas = datas.decode('utf-8')
		datas_split = datas.split('&')
		token = ''
		fs = 0
		wavs = []
		#type = 'wavfilebytes' # wavfilebytes or python-list
		
		for line in datas_split:
			[key, value]=line.split('=')
			if('wavs' == key and '' != value):
				wavs.append(int(value))
			elif('fs' == key):
				fs = int(value)
			elif('token' == key ):
				token = value
			#elif('type' == key):
			#	type = value
			else:
				print(key, value)
			
		if(token != 'qwertyuiop'):
			buf = '403'
			print(buf)
			buf = bytes(buf,encoding="utf-8")
			self.wfile.write(buf)  
			return
		
		#if('python-list' == type):
		if(len(wavs)>0):
			# print([wavs], fs)
			r = self.recognize([wavs], fs)
		else:
			r = ''
		#else:
		#	r = self.recognize_from_file('')
		
		if(token == 'qwertyuiop'):
			# buf = '成功\n'+'wavs:\n'+str(wavs)+'\nfs:\n'+str(fs)
			buf = r
		else:
			buf = '403'
		
		#print(datas)
		
		self._set_response()
		
		#buf = '<!DOCTYPE HTML> \n<html> \n<head>\n<title>Post page</title>\n</head> \n<body>Post Data:%s  <br />Path:%s\n</body>  \n</html>'%(datas,self.path)  
		print(buf)
		buf = bytes(buf,encoding="utf-8")
		self.wfile.write(buf)  
		
	def recognize(self, wavs, fs):
		r=''
		try:
			r_speech = ms.RecognizeSpeech(wavs, fs)
			print(r_speech)
			str_pinyin = r_speech
			r = ml.SpeechToText(str_pinyin)
		except:
			r=''
			print('[*Message] Server raise a bug. ')
		return r
		pass
	
	def recognize_from_file(self, filename):
		pass
		
def start_server():
	print('server start',host)
	sever = HTTPServer(host, HttpServerWB)
	sever.serve_forever()

if __name__ == '__main__':
	start_server()

