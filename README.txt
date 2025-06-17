

To launch it with background logging:
NOTE: You need to add the "affiliate ID" so that the links include the affiliate code, and MongoDB credentials to connect to the local MongoDB.
> nohup ./launcher.sh > logger_amz.log 2>&1 &


List of active services on the server using Python:
> ps aux | grep python

To monitor the logs:
> sudo tail -f logger_amz.log

To kill all processes:
> sudo killall python3








