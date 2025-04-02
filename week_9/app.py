import json
import time
import paho.mqtt.client as mqtt
from gpiozero import LED

id = 'ea16da5a-1155-4a0f-9e69-3283fa2413c9'

led = LED(26)

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'temperature_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    command = { 'led_on' : payload['temperature'] > 25 }
    print("Sending message:", command)

    if payload['temperature'] > 25:
        led.on()
    else:
        led.off()

    client.publish(server_command_topic, json.dumps(command))

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)