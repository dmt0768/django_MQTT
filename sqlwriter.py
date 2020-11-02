#!venv/bin/python3

from time import localtime, strftime, sleep
import paho.mqtt.client as mqtt
import sqlite3

topic_for_subscribe = "#"
log_topic = 'log'

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
    if msg.topic != log_topic:
        write_to_db(time, msg.topic, msg.payload.decode("utf-8"))

    return


def write_to_log(topic, message):
    client.publish(topic, message)
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    write_to_db(time, topic, message)
    print('write_to_log')


def topic_test(topic_id, on_none=True):

    if (topic_id is None) and on_none:
        raise sqlite3.Error('Topic not found')
    if (topic_id is not None) and not on_none:
        raise sqlite3.Error('Topic already exists')


def write_to_db(time, topic, message):
    try:
        topic_id = c.execute('SELECT type_id FROM core_types WHERE type = ?', (topic,)).fetchone()
        #  Запись сообщения
        if message[0] != '!':
            print("Ordinary message")
            topic_test(topic_id)
            c.execute("INSERT INTO core_messages ( message, time, type_id )" 
                      "VALUES(?, ?, ?);", (message, time, topic_id[0]))
            conn.commit()

        # Создание топика, если он отсутствует
        else:
            message = message[1:]
            if message == 'CREATE':
                topic_test(topic_id, on_none=False)
                c.execute("INSERT INTO core_types ( type )"
                          "VALUES(?);", (topic,))
                conn.commit()
                print('Created in database', topic)

        # Удаление топика
            elif message == 'REMOVE':
                topic_test(topic_id)
                c.execute("DELETE FROM core_types "
                          "WHERE type = ?;", (topic,))
                conn.commit()
                print('Removed', topic)
    except sqlite3.Error as err:
        # print(err.args)
        write_to_log(log_topic, str(err.args))


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
