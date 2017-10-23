import config
import pika
import json

arr = {'eui':'test',"timestamp":"2017-08-23T07:42:51.081853Z","stat":''}


credentials = pika.PlainCredentials(config.MQ_USER,config.MQ_PSWD)
conn_config = pika.ConnectionParameters(host=config.MQ_HOST, port=config.MQ_PORT,credentials=credentials)

connection = pika.BlockingConnection(conn_config)
channel = connection.channel()

channel.queue_declare(queue=config.MQ_QUEUE)
channel.basic_publish(exchange='',routing_key=config.MQ_QUEUE,body=json.dumps(arr))
connection.close()

def loop(i):
	connection = pika.BlockingConnection(conn_config)
	channel = connection.channel()

	channel.queue_declare(queue=config.MQ_QUEUE)
	arr['count'] = i
	channel.basic_publish(exchange='',routing_key=config.MQ_QUEUE,body=json.dumps(arr))
	connection.close()
	print('send message =====> '+str(i))

if __name__=='__main__':
	for i in range(1):
		loop(i)