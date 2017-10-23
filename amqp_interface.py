import config
import pika
from lss.cassandra.handler import store00
import json
def callback(ch,method,properties,body):
	try :
		nrr = {} 
		orr = json.loads(body)
		ks = orr.keys()
		for k in ks :
			if k not in ('eui','timestamp') :
				typ = k
		nrr = {
		'eui':orr['eui'],
		'tms':orr['timestamp'],
		'typ':typ,
		'msg':orr[typ]
		}
		store00(nrr)
	except Exception as err :
		print(err)
		pass


def setup_amqp():
	credentials = pika.PlainCredentials(config.MQ_USER,config.MQ_PSWD)

	conn_config = pika.ConnectionParameters(
			host = config.MQ_HOST,
			port = config.MQ_PORT,
			credentials=credentials
		)
	connection = pika.BlockingConnection(conn_config)
	channel = connection.channel()
	channel.queue_declare(queue=config.MQ_QUEUE)

	channel.basic_consume(callback,queue=config.MQ_QUEUE)
	
	print('Interface activated. To exit press CTRL+C')
	channel.start_consuming()

if __name__=='__main__':
	setup_amqp()