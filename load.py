import pymysql

HOST = "52.78.41.43"
PORT = 3306
USER = "lora"
PSWD = "fhfk1!"
DBNAME = "lora_account"

conn = pymysql.connect(
	host=HOST,
	port=PORT,
	user=USER,
	passwd=PSWD,
	db=DBNAME
	)

cur = conn.cursor()

query = 'select * from applications'

cur.execute(query)

for row in cur:
	print(row)




# ('hanapp', '', datetime.datetime(2018, 1, 22, 5, 35, 31), 'handler_ts1', '4367746c24215a395c2a7761', 'EFB1A3E886B6E1BB')
# ('test2', 'test2', datetime.datetime(2017, 11, 13, 12, 22, 49), 'handler2', '7e50533372743d3444616751', '70B3D57EF0000156')
# ('test3', '', datetime.datetime(2017, 11, 23, 17, 11, 17), 'handler_ts1', '7e50533372743d3444616751', 'E8ACA1E28BA0EC86')
# ('test_han_app', '', datetime.datetime(2018, 2, 21, 5, 40, 42), 'handler_ts1', '4367746c24215a395c2a7761', 'E1A983E585A0EE86')

