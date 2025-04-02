from gpiozero import LED
import time
import random
import paho.mqtt.client as mqtt
import json

led = LED(26)
id = 'ea16da5a-1155-4a0f-9e69-3283fa2413c9' #replace with your own unique id
client_telemetry_topic = id + '/telemetry'
client_name = id + '_temperature_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

def ds18b20Read():
	tfile = open("/sys/bus/w1/devices/28-3c01b556ec19/w1_slave")
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	temperature = round(temperature, 2)
	return temperature

mqtt_client.loop_start()

print("MQTT connected!")

while True:
    temperature = ds18b20Read()
    telemetry = json.dumps({'temperature' : temperature})
    print("Sending telemetry ", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(5)