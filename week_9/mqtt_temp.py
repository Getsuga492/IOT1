
import time
import paho.mqtt.client as mqtt

from gpiozero import LED
led = LED(26)


id = 'ea16da5a-1155-4a0f-9e69-3283fa2413c9' 
client_name = id + 'temperature_client'

def setup():
    mqtt_client = mqtt.Client(client_name)
    mqtt_client.connect('test.mosquitto.org')
    mqtt_client.loop_start() 
    print("MQTT connected!")

def ds18b20Read():
	tfile = open("/sys/bus/w1/devices/28-3c01b556ec19/w1_slave")
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	temperature = round(temperature, 2)
	if temperature > 25:
		led.on()
	else:
		led.off()
	print(temperature)
	return temperature

def loop():
	tmp = 0.0
	while True:
		tmp = ds18b20Read()
		time.sleep(3)
		
if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		print("Exiting...")

