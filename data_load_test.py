from cassandra.cqlengine import connection
import json, time, pyspark
from pyspark.sql import SparkSession
from datetime import date, timedelta, datetime

CONN_NM = 'analizer'
HOST = 'localhost'
KEYSPACE = 'lora_streaming_t'


sc = pyspark.SparkContext()
spark = SparkSession.builder.appName('queryfy').getOrCreate()

Query = {
	'get_last_stats' : 'select * from store00 where fid=12 and typ=\'stat\' and sdid=%s and tms >= %s allow filtering',
	'get_from_to_stat' : 'select * from store00 where fid=12 and typ=\'stat\' and sdid=%s and tms >= %s and tms <= %s allow filtering',
	'get_stats' : 'select * from store00 where fid=12 and typ=\'stat\' and tms >= %s allow filtering'
}

def db_set(keyspace):
	try:
		connection.set_default_connection(CONN_NM)
	except Exception as err:
		print('db set exception occured')
		connection.unregister_connection(HOST)
		connection.register_connection(CONN_NM, [HOST], default=True)
		connection.session.set_keyspace(keyspace)



def get_stats():
	db_set(KEYSPACE)

	strtoday = (date.today()+ timedelta(days=-1)).strftime('%Y-%m-%d')

	rows = connection.session.execute(Query['get_stats'],[strtoday])
	rdd = sc.parallelize(rows)

	rt_val = []
	if rdd.count() <= 0 :
		return rt_val
	else :
		df = rdd.toDF()
		df.createOrReplaceTempView('stat')
		sqldf = spark.sql("select * from stat where concat(sdid,'-',tms)  in (select max(concat(sdid,'-',tms))from stat group by sdid )")
		rows = sqldf.collect()
		for row in rows :
			item = row.asDict()
			item['tms'] = item['tms'].strftime('%Y-%m-%d %H:%M:%S') + ' GMT'
			rt_val.append(item)
	return rt_val
	

def get_list_stats(term, eui):
	db_set(KEYSPACE)
	# strtoday = date.today().strftime('%Y-%m-%d')
	# strtoday = '2017-01-05' # for test
	if term == 'day' :
		strtoday = (date.today()+ timedelta(days=-1)).strftime('%Y-%m-%d')
	elif term == 'week' :
		strtoday = (date.today()+ timedelta(weeks=-1)).strftime('%Y-%m-%d')
	elif term == 'month':
		strtoday = (date.today()+ timedelta(days=-31)).strftime('%Y-%m-%d')

	rows = connection.session.execute(Query['get_last_stats'],[eui, strtoday])
	rdd = sc.parallelize(rows)

	return mk_arr(rdd)

def get_from_to_stat(f,t,eui):
	f = f + ' 00:00:00'
	t = t + ' 23:59:59'
	from_dt = datetime.strptime(f,'%Y-%m-%d %H:%M:%S')
	to_dt = datetime.strptime(t,'%Y-%m-%d %H:%M:%S')

	rows = session.execute(Query['get_from_to_stat'],[eui, from_dt, to_dt])
	rdd = sc.parallelize(rows)

	return mk_arr(rdd)



def mk_arr(rdd):
	rt_val = []
	if rdd.count() <= 0 :
		return rt_val
	else :
		arr_length = int(rdd.count()/20)
		df = rdd.toDF()
		df.createOrReplaceTempView('stat')
		sqldf = spark.sql("select * from stat order by tms desc")
		rows = sqldf.collect()
		n = 0
		for row in rows :
			if n%arr_length == 0 :
				item = row.asDict()
				item['tms'] = item['tms'].strftime('%Y-%m-%d %H:%M:%S')
				rt_val.append(item)
			n = n + 1
	return rt_val

# for http
from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class GET_STAT(Resource):
	def get(self):
		rows = get_stats()
		return rows

class GET_LIST_STAT(Resource):
	def get(self, term, eui):
		rows = get_list_stats(term, eui)
		return rows

class GET_FROM_TO_STAT(Resource):
	def get(self, f, t, eui):
		rows = get_from_to_stat(f, t, eui)
		return rows

# rows = get_last_stats()
# 		if len(rows) > 0 :
api.add_resource(GET_FROM_TO_STAT, '/stat/term/<f>/<t>/<eui>')
api.add_resource(GET_LIST_STAT, '/stat/<term>/<eui>')
api.add_resource(GET_STAT, '/stat')

if __name__ == '__main__':
	app.run(debug=True)
	print('Server started as 5000')
