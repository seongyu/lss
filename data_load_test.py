from cassandra.cluster import Cluster
import json, time, pyspark
from pyspark.sql import SparkSession
from datetime import date, timedelta


HOST = ['localhost']
KEYSPACE = 'lora_streaming_t'


cluster = Cluster(HOST)
session = cluster.connect(KEYSPACE)
sc = pyspark.SparkContext()
spark = SparkSession.builder.appName('queryfy').getOrCreate()

Query = {
	'get_one_with_eui_typ' : 'select * from store01 where eui=%s and typ=%s limit 1 allow filtering',
	'get_last_stats' : 'select * from store01 where fid=12 and typ=\'stat\' and tms >= %s allow filtering'
}

def get_last_stats():
	# strtoday = date.today().strftime('%Y-%m-%d')
	# strtoday = '2017-01-05' # for test
	strtoday = (date.today()+ timedelta(days=-1)).strftime('%Y-%m-%d')

	rows = session.execute(Query['get_last_stats'],[strtoday])

	rdd = sc.parallelize(rows)
	df = rdd.toDF()
	returnv = []
	if df.count() <= 0 :
		return returnv
	else :
		df.createOrReplaceTempView('stat')
		sqldf = spark.sql("select * from stat where concat(sdid,'-',tms)  in (select max(concat(sdid,'-',tms))from stat group by sdid )")
		rows = sqldf.collect()
		for row in rows :
			item = row.asDict()
			item['tms'] = item['tms'].strftime('%Y-%M-%D %H:%m:%S')
			returnv.append(item)
	return returnv

def collect():
	jsonlist = []
	rows = get_stat()
	if len(rows) <= 0 :
		return rows	
	else :
		for row in rows:
			item = row.asDict()
			item['tms'] = item['tms'].strftime('%Y-%M-%D %H:%m:%S')
			jsonlist.append(item)
		return jsonlist

# for http
from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class GET_STAT(Resource):
	def get(self):
		rows = get_last_stats()
		return rows

class GET_LIST_STAT(Resource):
	def get(self, eui):
		print(eui)
		return 'testString'

# rows = get_last_stats()
# 		if len(rows) > 0 :
api.add_resource(GET_LIST_STAT, '/list/<eui>')
api.add_resource(GET_STAT, '/')

if __name__ == '__main__':
	app.run(debug=True)