import config
import pika
import json
from datetime import datetime
import pytz

arr = {'eui':'test',"timestamp":"2017-08-23T07:42:51.081853Z",'test':''}


credentials = pika.PlainCredentials(config.MQ_USER,config.MQ_PSWD)
conn_config = pika.ConnectionParameters(host=config.MQ_HOST, port=config.MQ_PORT,credentials=credentials)

def loop(i):
	connection = pika.BlockingConnection(conn_config)
	channel = connection.channel()

	channel.exchange_declare(exchange=config.MQ_QUEUE, exchange_type='fanout')

	# for test code ....
	time = datetime.now()
	arr['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
	arr['test'] = {'countsssss':i}

	channel.basic_publish(exchange=config.MQ_QUEUE,routing_key="",body=json.dumps(arr))
	connection.close()
	print('send message =====> ', arr['test'])

if __name__=='__main__':
	for i in range(1):
		loop(i)