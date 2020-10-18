# django_MQTT
It is an example of a server being MQTT-client, which can show MQTT messages via web-interface. SQLite is used as a database.

## Files description
- venv -- Python virtual environment

- server -- Django server file

- sqlwriter.py -- MQTT client program file (based on paho MQTT client). It subscribes to MQTT broker's topics and writes every new message in SQLite database in the file *server*

- start_total.py -- It just runs Django web-server with the only command without activating venv, etc... (*./start_total.py*)

## How to use

For propper using, you should connect your MQTT-client with MQTT-broker. Set new MQTT-server IP in *sqlwriter.py*. I used Mosquitto's broker on my PC, so the local server's IP is used.

1) Launch sqlwriter.py

```
./sqlwriter.py
```

2) Launch Django web-server

```
./start_total.py
```
