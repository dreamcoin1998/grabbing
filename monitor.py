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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import redis
from wx import send_move
import itchat
from buyjiu import buyjiu
from datetime import datetime



class MyEmail:
    def __init__(self, tag='页面已更新'):
        self.user = 'gaojunbin@gaoblog.cn'
        self.passwd = 'xfYC4mkT2QLPuBQv'
        self.to_list = ['1285338586@qq.com']
        self.cc_list = ['1285338586@qq.com']
        self.tag = tag
        self.html = 'res.html'

    def send(self):
        """
        发送邮件
        """
        try:
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
            server.login(self.user, self.passwd)
            server.sendmail("<%s>" % self.user, self.to_list, self.get_attach())
            server.close()
            print("send email successful")
        except Exception as e:
            print("send email failed %s" % e)

    def get_attach(self):
        """
        构造邮件内容
        """
        attach = MIMEMultipart()
        if self.tag is not None:
            # 主题,最上面的一行
            attach["Subject"] = self.tag
        if self.user is not None:
            # 显示在发件人
            attach["From"] = "<%s>" % self.user
        if self.to_list:
            # 收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            # 抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.html:
            # 估计任何文件都可以用base64，比如rar等
            # 文件名汉字用gbk编码代替
            name = os.path.basename(self.html).encode("utf8")
            f = open(self.html, "rb")
            html = MIMEText(f.read(), "html", "utf-8")
            attach.attach(html)
            f.close()
        return attach.as_string()


def get_info():
	r = redis.Redis(host='127.0.0.1', port=6379)
	res = r.lpop('mylist')
	if res is None:
		print('消息队列为空', res)
		return None
	else:
		data = eval(res.decode('utf8')) 
		# print(data)
	return data


def interface(enroll_date, proxy=None):
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
		# data = None
		data = get_info()
		# print(get_info())
		if data is None:
			# with open('res.html', 'w')as f:
				# f.write('未预约')
			# send_move('未预约')
			print('未预约')
		else:
			s = requests.Session()
			s.get('http://kwemobile.bceapp.com/maotai.php', headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=2)
			code = verify_2(s, proxy, headers)
			data['code'] = code
			data['enroll-date'] = enroll_date
			print(data)
			res = s.post('http://kwemobile.bceapp.com/maotai.php/index/addenroll.html', data=data, headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=2)
			with open(f'{data["name"]}{data["ticket"]}.html', 'wb')as f:
				f.write(res.content)
			# send_move('预约成功')
			# send_move(res.text)
		# email = MyEmail()
		# email.send()
		print('over')
	except Exception as e:
		print('出错', e)
		interface(enroll_date, proxy=proxy)


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
    return requests.get("http://www.gaoblog.cn:5010/get/").json()


#出错两次删除IP
def delete_proxy(proxy):
    requests.get("http://www.gaoblog.cn:5010/delete/?proxy={}".format(proxy))


# 获取监控状态
def test(proxy=None):
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
				res = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=2)
			else:
				res = requests.get(url, headers=headers)
			root = etree.HTML(res.content)
			date = root.xpath('//*[@id="enroll"]/fieldset/div[9]/div[3]/span/i/text()')
			status = root.xpath('//*[@id="enroll"]/fieldset/div[9]/div[3]/span/text()')
			print(date)
			print(status)
			return date, status
		except Exception as e:
			print('出错', e)
			retry_count -= 1
    # 出错2次, 删除代理池中代理
	delete_proxy(proxy)
	return None, None


def run(date, status):
	t1 = time.time()
	if status is not None:
		if len(status) != 0:
			# time.sleep(delta)
			while True:
				proxy = get_proxy().get("proxy")
				date_2, status_2 = test(proxy=proxy)
				if status_2 is not None:
					if len(status_2) != 0:
						print(status == status_2)
						# 信息不一致，页面更新，启动脚本
						if status_2 == status:
							print(int(time.time() - t1))
						# time.sleep(delta)
						else:
							for i, k in enumerate(status_2):
								if k != '已约满':
									enroll_date = date[i]
							# unittest.main()
							interface(enroll_date, proxy=proxy)
							# break
				else:
					print('为空')
					# time.sleep(delta)


def kucun():
	# true = True
	# false = False
	#time.sleep(0.5)
	proxy = get_proxy().get("proxy")
	retry_count = 2
	while retry_count > 0:
		try:
			headers = {
				'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57',
				'Referer': 'http://www.gzairports.com:11111/order/index.html?from=groupmessage&isappinstalled=0'
			}
			res = requests.post('http://www.gzairports.com:11111/searchOrderAppointmentSettings.action',
								headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=3)

			data = res.json()['result']['extend']['appointmentSettings'][0]
			if data['remainApoointmentPersonCountApart'] < 1 and data['remainApoointmentPersonCountDepart'] < 1:
				return True
			elif data['remainApoointmentPersonCountApart'] < 1:
				return True
			elif data['remainApoointmentPersonCountDepart'] < 1:
				return True
			return False
		except Exception as e:
			print('出错', e)
			retry_count -= 1
	# 出错2次, 删除代理池中代理
	delete_proxy(proxy)
	return kucun()


def main():
	# itchat.auto_login(hotReload=True)
	# delta = 0.5
	date, status = test()
	status = ['已约满', '已约满', '已约满', '已约满', '已约满', '已约满', '已约满', '已约满', '已约满', '已约满']
	for i in range(4):
		p = mp.Process(target=run, args=(date, status))
		p.start()
		print('进程开启')


def jk():
	while True:
		now = datetime.now()
		time = str(int(datetime.timestamp(now)))
		if kucun():
			print(time, '没货')
		else:
			print(time, '有库存')
			data = get_info()
			if data is None:
				print('未预约')
				continue
			if buyjiu(data):
				print('预约成功')
				email = MyEmail(tag='预约成功')
				email.send()
			else:
				email = MyEmail(tag='预约失败')
				email.send()


if __name__ == '__main__':
	# main()
	# unittest.main() # 时间点到主要运行这个直接启动脚本
	# interface()
	for i in range(4):
		p = mp.Process(target=jk, args=())
		p.start()
		print('进程开启')