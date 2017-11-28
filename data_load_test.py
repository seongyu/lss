from cassandra.cluster import Cluster
from websocket_server import WebsocketServer
import json, time
PORT = 30000

HOST = ['localhost']
KEYSPACE = 'lora_streaming_t'


cluster = Cluster(HOST)
session = cluster.connect(KEYSPACE)

Query = {
	'get_one_with_eui_typ' : 'select * from store00 where eui=%s and typ=%s limit 1 allow filtering'
}


def get_stat():
	rows = session.execute(Query['get_one_with_eui_typ'],['008000000000C6B1','stat'])
	row = rows[0]
	item = {
		'eui':row.eui,
		'tms':row.tms,
		'msg':json.loads(row.msg),
		'eui':row.eui,
		'eui':row.eui,
		'eui':row.eui
	}
	return row


def new_client(client,server):
	while True:
		time.sleep(1)

