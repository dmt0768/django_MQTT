#!venv/bin/python3

from time import localtime, strftime
import paho.mqtt.client as mqtt
import sqlite3

topic = "#"
dbFile = "server/db.sqlite3"

# Connect to database
conn = sqlite3.connect(dbFile)
c = conn.cursor()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())

    result = (time + "\t" + str(msg.payload))

    print(msg.topic + ":\t" + result)

    writeToDb(time, msg.topic, msg.payload.decode("utf-8"))

    return


def writeToDb(time, topic, message):
    if message[0] != '!':
        print("Writing to db...")
        c.execute("INSERT INTO core_messages ( message, time, topic_id )" 
                  "VALUES(?, ?, (SELECT topic_id FROM core_topics WHERE topic = ?));", (message, time, topic))
        conn.commit()
        print(topic)
        print(message[0])
    else:
        message = message[1:].split(' ')
        if message[0] == 'CREATE':
            print('create', message[1])
        elif message[0] == 'REMOVE':
            print('remove', message[1])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
