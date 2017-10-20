import config
import pika
import json

arr = {'eui':'test',"timestamp":"2017-08-11T07:42:51.081853Z","stat":''}


conn_config = pika.ConnectionParameters(host=config.MQ_HOST,port=config.MQ_PORT)
connection = pika.BlockingConnection(conn_config)
channel = connection.channel()

channel.queue_declare(queue=config.MQ_QUEUE)
channel.basic_publish(exchange='',routing_key=config.MQ_QUEUE,body=json.dumps(arr))
connection.close()