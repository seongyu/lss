from cassandra.cluster import Cluster
from websocket_server import WebsocketServer

import json, time

#import config
#HOST = config.HOST


HOST = ['localhost']
KEYSPACE = 'lora_streaming_t'
PORT = 30000

cluster = Cluster(HOST)
session = cluster.connect(KEYSPACE)

Query = {
	'get_devices_stat' : 'select * from store01 where fid=12 and typ=\'stat\' limit 1 allow filtering'
}

date.today().strftime('%Y-%m-%d')
def get_stat():
	rows = session.execute(Query['get_one_with_eui_typ'],['BR_1','stat'])
	try:
		row = rows[0]
		item = {
			'eui':row.eui,
			'timestamp':row.tms.strftime('%Y-%m-%d %H:%M:%S'),
			'flow_id':row.fid,
			'receive_component_id':row.rcid,
			'send_component_id':row.sdid,
			'msg':json.loads(row.msg)
		}
	except:
		item = {
		'msg':'No data'
		}
	return item


def new_client(client,server):
	n = 0
	while True:
		time.sleep(10)
		row = get_stat()
		print('send row : ',n)
		n = n+1
		server.send_message_to_all(json.dumps(row))

def client_left(client, server):
	print("Client(%d) disconnected", client)

server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
print('Websocket Server Started...')
server.run_forever()