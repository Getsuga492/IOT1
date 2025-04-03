import time
import paho.mqtt.client as mqtt
import json
from gpiozero import LED

id = 'ea16da5a-1155-4a0f-9e69-3283fa2413c9'  # Replace with your own unique ID

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + '_temperature_client'

led = LED(26) 

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

# Function to handle incoming commands
def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Command received:", payload)

    if payload.get("led_on"): 
        led.on()
    else:
        led.off()

# Read temperature from the sensor
def ds18b20Read():
    tfile = open("/sys/bus/w1/devices/28-3c01b556ec19/w1_slave")
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:]) / 1000
    return round(temperature, 2)

# Subscribe to receive commands
mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command  # Assign message handler
mqtt_client.loop_start()

print("MQTT connected!")

while True:
    temperature = ds18b20Read()
    telemetry = json.dumps({'temperature': temperature})
    print("Sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(5)
