import config
from lss.util import logging
import pika
from lss.cassandra.handler import store00
import json

logger = logging.getLogger()

if config.DTP=='D':
	logger.setLevel(logging.DEBUG)
elif config.DTP=='T':
	logger.setLevel(logging.INFO)
else :
	logger.setLevel(logging.ERROR)


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
		logger.info(nrr)
		store00(nrr)
	except Exception as err :
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
	channel.exchange_declare(exchange=config.MQ_QUEUE,exchange_type='fanout')

	result = channel.queue_declare(exclusive=True)
	queue_name = result.method.queue
	channel.queue_bind(exchange=config.MQ_QUEUE, queue=queue_name)

	# channel.queue_bind(exchange=config.MQ_QUEUE,queue=config.MQ_QUEUE)

	channel.basic_consume(callback,queue=queue_name,no_ack=True)
	
	print('Interface activated. To exit press CTRL+C')
	channel.start_consuming()

if __name__=='__main__':
	setup_amqp()