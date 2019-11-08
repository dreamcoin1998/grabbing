import requests
import re
import time


def get_telNumber():
    res = requests.get('http://120.79.137.205:9180/service.asmx/GetHM2Str?token=9A2E80142F442DD23507828881BF38A6&xmid=295&sl=1&lx=6&a1=&a2=&pk=&ks=0&rj=')
    haoma = res.text.replace('hm=', '')
    print(haoma)
    return haoma


def get_smsCode(haoma):
    # res = requests.get('http://120.79.137.205:9180/service.asmx/UserLoginStr?name=1285338586&psw=18759799353gjb')
    # token = res.text
    url = f'http://120.79.137.205:9180/service.asmx/GetYzm2Str?token=9A2E80142F442DD23507828881BF38A6&xmid=295&hm={haoma}&sf=1'
    res = requests.get(url)
    while len(res.text) < 4:
        if res.text == '1':
            time.sleep(2)
            res = requests.get(url)
        else:
            print('短信验证出错', res.text)
            return None
    code = re.match(r'【\w+】\w+：(\d{6})，\w+\d\w+，\w+，\w+。', res.text).groups()[0]
    return code


def send_yzm(s, telNumber, startStation, terminalStation):
    data = {'telNumber': telNumber, 'startStation': startStation, 'terminalStation': terminalStation}
    res = s.post('http://www.gzairports.com:11111/sendSms.action', data=data)
    return res.json()['result']['success']