from cassandra.cluster import Cluster
import time

HOST = ['localhost']
KEYSPACE = 'lora_streaming_t'


cluster = Cluster(HOST)
session = cluster.connect(KEYSPACE)

Query = {
	'get_one_with_eui_typ' : 'select * from store00 where eui=%s and typ=%s limit 1 allow filtering'
}




if __name__=='__main__':
	n = 0
	try :
		while True :
			rows = session.execute(Query['get_one_with_eui_typ'],['008000000000C6B1','stat'])
			n = n+1
			print('=================== QUERY COUNT :',n,'===================')
			print(rows[0])
			print('==============',time.ctime(),'===============')
			time.sleep(60)
	except Exception as err:
		print(err)