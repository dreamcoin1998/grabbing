import redis
import config
import logging


r = redis.Redis(host='127.0.0.1', port=6379)
# r = redis.StrictRedis(host='0.0.0.0', port=6379)
# 如果要指定数据库，则 r = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)
def push_1(data=None):
	if data is None:
		data = str({'member': config.menber,
				 'name': config.name,
				 'id-card': config.id_card,
				 'tel': config.tel,
				 'ticket': config.ticket,
				 'setoff': config.setoff,
				 'arrive': config.arrive,
				 'flt-date': config.flt_date,
				 'enroll-date': config.enroll_date,
				 'service': 'on',
				 'secret': 'on'})
	r.rpush('yuyue', data)


def push_2(data=None):
	if data is None:
		data = str(
			{
				'userName': config.userName,
				'idCard': config.idCard,
				'airways': config.airways,
				'flightNo': config.flightNo,
				'startStation': config.startStation,
				'terminalStation': config.terminalStation,
				'flightDate': config.flightDate,
				# 'telNumber': config.telNumber,
				'appointCount': config.appointCount,
			}
		)
	logging.info('添加进消息队列' + data)
	r.rpush('mylist', data)


def get():
	r = redis.Redis(host='127.0.0.1', port=6379)
	res = r.lpop('yuyue')
	data = eval(res.decode('utf8'))
	if data.get('enroll_date') is not None:
		data['enroll-date'] = data.pop('enroll_date')
		push_1(str(data))
		get()
	# print(data)


if __name__ == '__main__':
	# push_2()
	push_1()
	# get()