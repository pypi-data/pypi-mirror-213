import json
import os
import time

from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from paho.mqtt import client as mqtt

from easysmart.utils import start_emqx_server
from easysmart.mdns import mdns_register


def on_log(client, userdata, level, buf):
    if level == MQTT_LOG_INFO:
        head = 'INFO'
    elif level == MQTT_LOG_NOTICE:
        head = 'NOTICE'
    elif level == MQTT_LOG_WARNING:
        head = 'WARN'
    elif level == MQTT_LOG_ERR:
        head = 'ERR'
    elif level == MQTT_LOG_DEBUG:
        head = 'DEBUG'
    else:
        head = level
    print('%s: %s' % (head, buf))


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    # client.subscribe(topic, 0)


def on_message(client, userdata, msg):
    print('topic:' + msg.topic + ' ' + str(msg.payload))
    try:
        data = json.loads(msg.payload)
    except:
        data = str(msg.payload)
    print(f'{data}')


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected disconnection %s' % rc)


class Manager:

    def __init__(self):
        start_emqx_server()
        mdns_register()
        self.client_id = 'MQTT_MAIN' + os.urandom(6).hex()
        self.client = mqtt.Client(self.client_id, protocol=mqtt.MQTTv311, clean_session=False)
        self.client.on_log = on_log
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect
        self.client.connect('mqtt_server.local', 1883, 60)
        self.client.loop_start()
        self.client.subscribe('#', 0)
        self.client.subscribe('device/#', 1)
        self.client.subscribe('all/', 1)
        self.client.subscribe('test/', 1)
        self.client.publish('test', 'hello world', 0)

    def subscribe(self, *args, **kwargs):
        return self.client.subscribe(*args, **kwargs)

    def publish(self, *args, **kwargs):
        return self.client.publish(*args, **kwargs)

    def loop_forever(self):
        return self.client.loop_forever()

    def loop_start(self):
        return self.client.loop_start()


if __name__ == '__main__':
    m = Manager()
    while True:
        time.sleep(1)
