#!venv/bin/python3

from time import localtime, strftime, sleep
import paho.mqtt.client as mqtt
import sqlite3

topic_for_subscribe = "user/#"
log_topic = 'system/log'

data_base = "server/db.sqlite3"

# Connect to database
conn = sqlite3.connect(data_base)
c = conn.cursor()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_for_subscribe)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())

    result = (time + "\t" + str(msg.payload))

    print(msg.topic + ":\t" + result)

    writeToDb(time, msg.topic, msg.payload.decode("utf-8"))

    return


def write_to_log(topic, message):
    client.publish(topic, message)
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    writeToDb(time, topic, message)
    print('write_to_log')


def writeToDb(time, topic, message):
    try:
        #  Запись сообщения
        if message[0] != '!':
            print("Writing to db...")
            c.execute("INSERT INTO core_messages ( message, time, topic_id )" 
                      "VALUES(?, ?, (SELECT topic_id FROM core_topics WHERE topic = ?));", (message, time, topic))
            conn.commit()
            print('Finished!')

        # Создание топика, если он отсутствует
        else:
            message = message[1:]
            if message == 'CREATE':
                c.execute("INSERT INTO core_topics ( topic )"
                          "VALUES(?);", (topic,))
                conn.commit()
                print('Created in database', topic)

        # Удаление топика
            elif message == 'REMOVE':
                c.execute("DELETE FROM core_topics "
                          "WHERE topic = ?;", (topic,))
                conn.commit()
                print('removed', topic)
    except sqlite3.Error as err:
        print(err.args)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.on_publish = on_publish

client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
