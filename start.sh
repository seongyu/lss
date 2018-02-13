#! /bin/bash

process_id=`ps aux| grep amqp_interface | grep -v "grep" | awk '{print $2}'`

case $1 in
	"start")
		echo 'Kill previous processes'
		kill -9 $process_id
		echo '=== Start lss service ==='
		python3 amqp_interface.py &
		echo 'Successfully started >>>';;
	"stop")
		echo '=== Kill AMQP Interface process ==='
		kill -9 $process_id
		echo 'Successfully killed >>>';;
	*)
		echo 'Missing command. Input command start/stop';;
esac