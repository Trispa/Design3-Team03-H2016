#!/bin/sh
IP="$(ifconfig wlp3s0 | grep "inet addr" | cut -d ':' -f 2 | cut -d ' ' -f 1)"
echo "{\n    \"url\":\""$IP"\",\n    \"port\":\"9000\"\n}" > Shared/config.json

echo "Press enter once finish!"
read input_variable

cd Server
konsole -e node broadcaster.js &

echo "Press enter once finish!"
read input_variable

cd ..
firefox --new-window "${IP}":9000 &
python2.7 -m Client.BaseStation.BaseClientSocketScript.py

