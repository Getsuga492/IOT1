import json
import time
import paho.mqtt.client as mqtt

id = 'ea16da5a-1155-4a0f-9e69-3283fa2413c9'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + '_temperature_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

# Function to process telemetry and send LED command
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    
    command = { 'led_on': payload['temperature'] > 27 }  # Logic for LED
    print("Sending command:", command)
    
    client.publish(server_command_topic, json.dumps(command))  # Send command

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)