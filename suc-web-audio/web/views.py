from django.shortcuts import render
from django.http.response import HttpResponse
import time
import os
from general_function.file_wav import *
import requests
import json
# Create your views here.



UPLOAD_ROOT = './upload/'
AUDIO_SERVER_URL = 'http://127.0.0.1:8888/'
def index(request):
	return render(request,'index.html')


def login(request):
		if request.method == "POST":
			print(request.body)
			username = request.POST.get('username')
			password = request.POST.get('password')
			print(username,password)
			return HttpResponse(username)
		else:
			return HttpResponse(403)


def uploadFile(request):
	if request.method == 'POST':
		file = request.FILES.get('file')
		print(file)
		if file:
			res = savefile(file)
			return HttpResponse(json.dumps(res))
		else:
			return HttpResponse(json.dumps({'status':400,'message':'服务异常'}))
	else:
		return HttpResponse(json.dumps({'status':403,'message':'错误访问'}))


def savefile(file):
	try:
		## 保存文件
		day_dir = time.strftime('%Y%m%d')
		last_dir = os.path.join(UPLOAD_ROOT,day_dir)
		if not os.path.exists(last_dir):
			os.makedirs(last_dir)
		fileName = file.name
		filePath = os.path.join(last_dir,fileName)
		print(filePath)
		with open(filePath,'wb') as f:
					for line in file.chunks():
						f.write(line)

		##转化数据
		wavsignal,fs=read_wav_data(filePath)
		print(wavsignal,fs)
		token = 'qwertyuiop'
		datas={'token':token, 'fs':fs, 'wavs':wavsignal}
		r = requests.post(AUDIO_SERVER_URL, datas)
		r.encoding='utf-8'
		return {'status':200,'message':str(r.text)}
	except Exception as e:
		print('服务异常',e)
	return {'status':400,'message':'服务异常，请检查模型服务'}
	
