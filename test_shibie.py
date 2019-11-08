import requests
from datetime import datetime
import hashlib
import base64
import random
import json


# 这里本来想截取验证码图片，然后传到这里识别的，但是截取不到，只能模拟刷新验证码传过来识别
# 获取页面session刷新并提取验证码图片并且识别验证码
def verify(items):
	url = 'http://kwemobile.bceapp.com/maotai.php/index/verify?time=' + str(random.random())
	s = requests.Session()
	cookie = {}
	for item in items:
		s.cookies.set(item['name'],item['value'])
		cookie[item['name']] = item['value']
	print(s.cookies)
	# headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
	now = datetime.now()
	time = str(int(datetime.timestamp(now)))
	userID = '118006'
	pd_key = 'Fhq9N8NsY7M3TEQ6HonzKCaXDX3nuHa7'
	predict_type = '40500'
	md5 = hashlib.md5()
	md5.update(f'{time}{pd_key}'.encode('utf-8'))
	n = md5.hexdigest()
	md5 = hashlib.md5()
	md5.update(f'{userID}{time}{n}'.encode('utf-8'))
	sign = md5.hexdigest()
	res = s.get(url)
	b64 = base64.b64encode(res.content)
	img_data = b64.decode('utf-8')
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	data = {'user_id': userID, 'timestamp': time, 'sign': sign, 'predict_type': predict_type, 'img_data': img_data}
	res = requests.post('http://pred.fateadm.com/api/capreg', data=data, headers=headers)
	print(res.text)
	print(json.loads(res.json().get('RspData')).get('result'))
	return json.loads(res.json().get('RspData')).get('result')


# 参数：一个requests.Session对象, 代理IP
def verify_2(s, headers):
	now = datetime.now()
	time = str(int(datetime.timestamp(now)))
	url = 'http://www.gzairports.com:11111/order/creatImgCode.action?d=' + time
	print(s.cookies)
	userID = '118006'
	pd_key = 'Fhq9N8NsY7M3TEQ6HonzKCaXDX3nuHa7'
	predict_type = '40500'
	md5 = hashlib.md5()
	md5.update(f'{time}{pd_key}'.encode('utf-8'))
	n = md5.hexdigest()
	md5 = hashlib.md5()
	md5.update(f'{userID}{time}{n}'.encode('utf-8'))
	sign = md5.hexdigest()
	res = s.get(url, headers=headers, timeout=2)
	with open('a.png', 'wb')as w:
		w.write(res.content)
	b64 = base64.b64encode(res.content)
	img_data = b64.decode('utf-8')
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	data = {'user_id': userID, 'timestamp': time, 'sign': sign, 'predict_type': predict_type, 'img_data': img_data}
	res = requests.post('http://pred.fateadm.com/api/capreg', data=data, headers=headers)
	print(res.text)
	print(json.loads(res.json().get('RspData')).get('result'))
	return json.loads(res.json().get('RspData')).get('result')

# verify('code.png')


def verrify_3(content):
	now = datetime.now()
	time = str(int(datetime.timestamp(now)))
	userID = '118006'
	pd_key = 'Fhq9N8NsY7M3TEQ6HonzKCaXDX3nuHa7'
	predict_type = '40500'
	md5 = hashlib.md5()
	md5.update(f'{time}{pd_key}'.encode('utf-8'))
	n = md5.hexdigest()
	md5 = hashlib.md5()
	md5.update(f'{userID}{time}{n}'.encode('utf-8'))
	sign = md5.hexdigest()
	b64 = base64.b64encode(content)
	img_data = b64.decode('utf-8')
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	data = {'user_id': userID, 'timestamp': time, 'sign': sign, 'predict_type': predict_type, 'img_data': img_data}
	res = requests.post('http://pred.fateadm.com/api/capreg', data=data, headers=headers)
	print(res.text)
	print(json.loads(res.json().get('RspData')).get('result'))
	return json.loads(res.json().get('RspData')).get('result')