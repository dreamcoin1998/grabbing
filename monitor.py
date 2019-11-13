import requests
import random
from lxml import etree
import time
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from selenium.webdriver.chrome.options import Options
from test_shibie import verify, verify_2
try:
    from PIL import Image
except ImportError:
    import Image
import config
import redis
from wx import send_move
import itchat
from buyjiu import buyjiu
from datetime import datetime
from push import push_1, push_2
import logging
from send_email import MyEmail
from requests.adapters import HTTPAdapter


def get_info():
	r = redis.Redis(host='127.0.0.1', port=6379)
	res = r.lpop('mylist')
	if res is None:
		logging.info('买酒 消息队列为空')
		return None
	else:
		data = eval(res.decode('utf8'))
		logging.info('消息：' + data)
		# print(data)
	return data


def get_yuyue():
	r = redis.Redis(host='127.0.0.1', port=6379)
	res = r.lpop('yuyue')
	if res is None:
		print('消息队列为空')
		return None
	else:
		data = eval(res.decode('utf8'))
		# print(data)
	return data


def interface(data, proxy=None):
	try:
		# itchat.auto_login(hotReload=True)
		# url = 'http://kwemobile.bceapp.com/maotai.php/index/verify?time=' + str(random.random())
		User_Agent = ['Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
				'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
				'Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
				'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN',
				'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57'
				]
		if proxy is None:
			proxy = get_proxy().get("proxy")
		headers = {'User-Agent': random.choice(User_Agent)}
		s = requests.Session()
		s.get('http://kwemobile.bceapp.com/maotai.php', headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=3)
		code = verify_2(s, proxy, headers)
		data['code'] = code
		print(data)
		res = s.post('http://kwemobile.bceapp.com/maotai.php/index/addenroll.html', data=data, headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=3)
		with open(f'{data["name"]}{data["ticket"]}.html', 'wb')as f:
			f.write(res.content)
		# send_move('预约成功')
		# send_move(res.text)
		logging.info('预约成功')
		email = MyEmail(tag=f'{data["name"]} 预约成功', html=f'{data["name"]}{data["ticket"]}.html')
		email.send()
		return 0
	except Exception as e:
		push_1(data=str(data))
		print('出错', e)
		logging.error(e)
		# interface(data)
		return 1


# 你发的脚本
class UntitledTestCase(unittest.TestCase):
    def setUp(self):
    	chrome_options = Options()
    	chrome_options.add_argument("--disable-extensions")
    	chrome_options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})
    	self.driver = webdriver.Chrome(chrome_options=chrome_options)
    	self.driver.implicitly_wait(30)
    	self.base_url = "https://www.katalon.com/"
    	self.verificationErrors = []
    	self.accept_next_alert = True

    def test_untitled_test_case(self):
    	driver = self.driver
    	driver.get("http://kwemobile.bceapp.com/maotai.php")
    	# driver.find_element_by_xpath('//*[@id="enroll"]/fieldset/img')
    	# print(driver.get_cookies())
    	time.sleep(11)
    	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='《活动须知》'])[2]/following::span[1]").click()
    	# time.sleep(5)
    	# driver.find_element_by_xpath('//*[@id="member"]').click()
    	driver.find_element_by_id("member").click()
    	Select(driver.find_element_by_id("member")).select_by_visible_text(config.menber)
    	driver.find_element_by_id("name").click()
    	driver.find_element_by_id("name").clear()
    	driver.find_element_by_id("name").send_keys(config.name)
    	driver.find_element_by_id("id-card").click()
    	driver.find_element_by_id("id-card").clear()
    	driver.find_element_by_id("id-card").send_keys(config.id_card)
    	driver.find_element_by_id("tel").click()
    	driver.find_element_by_id("tel").clear()
    	driver.find_element_by_id("tel").send_keys(config.tel)
    	driver.find_element_by_id("ticket").click()
    	driver.find_element_by_id("ticket").clear()
    	driver.find_element_by_id("ticket").send_keys(config.ticket)
    	driver.find_element_by_id("setoff").clear()
    	driver.find_element_by_id("setoff").click()
    	driver.find_element_by_id("setoff").send_keys(config.setoff)
    	driver.find_element_by_id("arrive").click()
    	driver.find_element_by_id("arrive").clear()
    	driver.find_element_by_id("arrive").send_keys(config.arrive)
    	driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='- 说明：仅限乘机后7天内报名参与活动'])[1]/following::span[1]").click()
    	driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='验证码:'])[1]/preceding::span[1]").click()
    	# time.sleep(5)
    	time.sleep(10)
    	driver.find_element_by_id("code").click()
    	driver.find_element_by_id("code").clear()
    	# key = verify()
    	print(driver.get_cookies())
    	key = verify(driver.get_cookies())
    	print(key)
    	driver.find_element_by_id("code").send_keys(key)
    	time.sleep(10)
    	driver.find_element_by_id("service").click()
    	driver.find_element_by_id("secret").click()
    	driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='《用户条款&隐私协议》'])[1]/following::button[1]").click()
    	time.sleep(300)


# 获取代理IP
def get_proxy():
	try:
		return requests.get("http://www.gaoblog.cn:5010/get/").json()
	except Exception as e:
		logging.error(e)
		return {'proxy': None}

#出错两次删除IP
def delete_proxy(proxy):
	try:
		requests.get("http://www.gaoblog.cn:5010/delete/?proxy={}".format(proxy))
	except Exception as e:
		logging.error(e)
		pass


# 获取监控状态
def test(proxy=None):
	requests.adapters.DEFAULT_RETRIES = 3
	s = requests.session()
	s.keep_alive = False
	retry_count = 2
	User_Agent = ['Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
			'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
			'Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
			'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN',
			'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57'
			]
	headers = {'User-Agent': random.choice(User_Agent)}
	url = 'http://kwemobile.bceapp.com/maotai.php?from=groupmessage&isappinstalled=0'
	while retry_count > 0:
		try:
			if proxy:
				res = s.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=3)
			else:
				res = s.get(url, headers=headers)
			# print(res.text)
			# with open('res.html', 'w')as f:
				# f.write(res.text)
			root = etree.HTML(res.content)
			date = root.xpath('//*[@id="enroll"]/fieldset/div[9]/div[2]/span/i/text()')
			status = root.xpath('//*[@id="enroll"]/fieldset/div[9]/div[2]/span/text()')
			# print(date)
			# print(status)
			dic = {}
			for i in range(len(date)):
				dic[date[i]] = status[i]
			print(dic)
			return dic
		except Exception as e:
			print('出错', e)
			# logging.error(e)
			retry_count -= 1
    # 出错2次, 删除代理池中代理
	delete_proxy(proxy)
	return None


def run(dic):
	t1 = time.time()
	if dic != {}:
		while True:
			proxy = get_proxy().get("proxy")
			print(proxy)
			dic_2 = test(proxy=proxy)
			dic_2 = {'11月21日 下午': '可预约'}
			if dic_2 != {} and dic_2 is not None:
				print(dic == dic_2)
				# 信息不一致，页面更新，启动脚本
				if dic == dic_2:
					print(int(time.time() - t1))
				# time.sleep(delta)
				else:
					data = get_yuyue()
					if data is not None:
						logging.info(str(t1) + ' 页面已更新')
						if data['enroll-date'] == []:
							logging.info('不指定日期')
							for k, v in dic_2.items():
								if v != '已约满':
									data['enroll-date'] = k
							# unittest.main(
							interface(data, proxy=proxy)
						else:
							### 轮询的方式
							dates = data.get('enroll-date')
							for day in dates:
								status = dic_2.get(day)
								# logging.info('当日状态：' + status)
								if status != '已约满':
									data['enroll-date'] = day
									interface(data, proxy=proxy)
									break
						push_1(data=str(data))
					else:
						print('未预约')
			else:
				# delete_proxy(proxy)
				# print('删除代理')
				print('为空')
				# time.sleep(delta)


def kucun():
	# true = True
	# false = False
	#time.sleep(0.5)
	# requests.adapters.DEFAULT_RETRIES = 5
	proxy = get_proxy().get("proxy")
	# print(proxy)
	retry_count = 2
	retry_times = 2
	while retry_count > 0 and retry_times > 0:
		time.sleep(0.3)
		try:
			User_Agent = [
				'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
				'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
				'Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
				'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN',
				'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57'
				]
			headers = {'User-Agent': random.choice(User_Agent)}
			res = requests.post('http://www.gzairports.com:11111/searchOrderAppointmentSettings.action',
								headers=headers, proxies={"https": "https://{}".format(proxy)}, timeout=2)
			# print(res.text)
			data = res.json()['result']['extend']['appointmentSettings'][0]
			if data['remainApoointmentPersonCountApart'] < 1 and data['remainApoointmentPersonCountDepart'] < 1:
				return True
			elif data['remainApoointmentPersonCountApart'] < 1:
				return True
			elif data['remainApoointmentPersonCountDepart'] < 1:
				return True
			return False
		except requests.exceptions.ReadTimeout as e:
			print('连接问题', e)
			retry_count -= 1
		except requests.exceptions.ConnectTimeout as e:
			print('连接问题', e)
			retry_count -= 1
		except requests.exceptions.ProxyError as e:
			print('连接问题', e)
			retry_count -= 1
		except Exception as e:
			print('崩了', e, '代理为', proxy)
			retry_times -= 1
	# 出错2次, 删除代理池中代理
	if retry_count == 0:
		delete_proxy(proxy)
	return kucun()


def jk():
	while True:
		now = datetime.now()
		time = str(int(datetime.timestamp(now)))
		if kucun():
			print(time, '没货')
			# logging.info(time + '没货')
		else:
			logging.info(time + '有库存')
			print(time, '有库存')
			data = get_info()
			if data is None:
				print('未预约')
				logging.info('未预约')
				continue
			if buyjiu(data):
				logging.info(data['userName'] + ':预约成功')
				print('预约成功')
				email = MyEmail(tag=data['userName'] + ': 预约成功')
				email.send()
			else:
				logging.info(data['userName'] + ':预约失败')
				print('预约失败')
				push_2(data=data) # 预约失败重新添加进消息队列
				email = MyEmail(tag=data['userName'] + ':预约失败')
				email.send()
			logging.info('=======================')


def main():
	# itchat.auto_login(hotReload=True)
	# delta = 0.5
	logging.basicConfig(filename='yuyue.log', level=logging.INFO)
	proxy = get_proxy().get("proxy")
	print(proxy)
	dic = test(proxy=proxy)
	for i in range(4):
		p = mp.Process(target=run, args=(dic,))
		p.start()
		print('进程开启')


def main_2():
	logging.basicConfig(filename='main.log', level=logging.INFO)
	for i in range(4):
		p = mp.Process(target=jk, args=())
		p.start()
		print('进程开启')


if __name__ == '__main__':
	main()
	# unittest.main() # 时间点到主要运行这个直接启动脚本
	# interface('11月15日 下午')
	# data = get_info()
	# buyjiu(data)
	# main_2()