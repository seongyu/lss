import config
import pika

def callback(ch,method,properties,body):
	print(ch,method,properties,body)

def setup_amqp():
	conn_config = pika.ConnectionParameters(
			host = config.MQ_HOST,
			port = config.MQ_PORT
		)
	connection = pika.BlockingConnection(conn_config)
	channel = connection.channel()
	channel.queue_declare(queue=config.MQ_QUEUE)

	channel.basic_consume(callback,queue=config.MQ_QUEUE,no_ack=True)
	
	print('Interface activated. To exit press CTRL+C')
	channel.start_consuming()

if __name__=='__main__':
	setup_amqp()