from cassandra.cluster import Cluster
from websocket_server import WebsocketServer
import json, time
PORT = 30000

HOST = ['localhost']
KEYSPACE = 'lora_streaming_t'


cluster = Cluster(HOST)
session = cluster.connect(KEYSPACE)

Query = {
	'get_one_with_eui_typ' : 'select * from store01 where eui=%s and typ=%s limit 1 allow filtering'
}


def get_stat():
	rows = session.execute(Query['get_one_with_eui_typ'],('000C05FFFE7205E1','stat'))
	try:
		row = rows[0]
		item = {
			'eui':row.eui,
			'timestamp':row.tms,
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
	while True:
		time.sleep(1)
		row = get_stat()
		server.send_message_to_all(json.dumps(row))

def client_left(client, server):
	print("Client(%d) disconnected", client['id'])

server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
print('Websocket Server Started...')
server.run_forever()