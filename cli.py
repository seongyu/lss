import config
import pika
import json
from datetime import datetime
import pytz

arr = {'eui':'test',"timestamp":"2018-01-1T07:42:51.081853Z",'test':''}

arr1 = {'eui': 'broker2', 'timestamp': '2017-12-21T17:09:55.055Z', 'flow_id': 54, 'recv_component_id': 'broker2', 'send_component_id': 'handler2', 'message': {'BrokerDownlinkMessage':{'devId': 'test2_1', 'brokerId': 'broker2', 'payload': 'YNEAACYgawAGohGR', 'handlerId': 'handler2', 'appId': 'test2', 'DownlinkOption': {'bridgeId': 'Bridge1', 'modulation': 'LORA', 'routerId': 'router2', 'codingRate': '4/5', 'rfChain': 0, 'dataRate': 'SF10BW125', 'power': 0, 'deadline': 1513843796344, 'tmst': 1000003, 'gatewayId': 'TEST1', 'frequency': 922100000}, 'appEui': 'ECB2A5EB8F9DEF8A', 'devEui': 'EAAB9BEAB0B4E480'}}}


credentials = pika.PlainCredentials(config.MQ_USER,config.MQ_PSWD)
conn_config = pika.ConnectionParameters(host=config.MQ_HOST, port=config.MQ_PORT,credentials=credentials)

def loop(i):
	connection = pika.BlockingConnection(conn_config)
	channel = connection.channel()

	channel.exchange_declare(exchange=config.MQ_QUEUE, exchange_type='fanout')

	# for test code ....
	time = datetime.now()
	arr1['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
	

	channel.basic_publish(exchange=config.MQ_QUEUE,routing_key="",body=json.dumps(arr1))
	connection.close()
	print('send message =====> ', arr['test'])

if __name__=='__main__':
	for i in range(1):
		loop(i)