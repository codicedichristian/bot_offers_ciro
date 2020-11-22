
per lanciarlo con i log in background:
nohup ./launcher.sh > logger_amz.log 2>&1 &

lista servizi attivi nel server con python
ps aux | grep python

per controllare i log: 
sudo tail -f logger_amz.log

per killare tutto: 
sudo killall python3
