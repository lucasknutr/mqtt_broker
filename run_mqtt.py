import paho.mqtt.client as mqtt
import time

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, reason_code):
    print(f"Connected to broker with code: {reason_code}")
    # Subscribe to the topic when connected
    client.subscribe("sg2000")

# Callback when a message is received from the broker
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode('utf-8')}' on topic '{message.topic}'")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
broker_address = "broker.hivemq.com"
broker_port = 1883
client.connect(broker_address, broker_port)

# Start the client loop in a separate thread
client.loop_start()

# Publish messages to the topic
publish_topic = "sg1000"
alert_message = "alerta"
desarm_message = "desarme"

# Give the client time to connect
time.sleep(1)

print(f"Publishing '{alert_message}' to topic '{publish_topic}'")
client.publish(publish_topic, alert_message)

# Keep the alarm active for 10 seconds
alarm_duration = 10
time.sleep(alarm_duration)

print(f"Publishing '{desarm_message}' to topic '{publish_topic}' to stop the alarm")
client.publish(publish_topic, desarm_message)

# Keep the script running to receive messages
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")

# Stop the loop and disconnect the client
client.loop_stop()
client.disconnect()
