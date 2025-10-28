#Shivangi Gakhar
#123CS0167
from umqtt.simple import MQTTClient
from machine import Pin,time_pulse_us
import network
import ujson
import time
import dht

# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
LED_TOPIC = "mqtt-demoShivangi/led"
LED_TOPIC2 = "mqtt-demoShivangi/led2"
IR_TOPIC="mqtt-demoShivangi/ir"
ULTRASONIC_TOPIC = "mqtt-demoShivangi/ultra"
CLIENT_ID = "mark-mqtt-demoShivangi"

dht_sensor = dht.DHT22(Pin(33))
onboard_led = Pin(23, Pin.OUT)
onboard_led2 = Pin(16, Pin.OUT)
pir_sensor = Pin(2, Pin.IN)
THRESHOLD=15
trigger=Pin(4,Pin.OUT)
echo=Pin(32,Pin.IN)

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect('Wokwi-GUEST', '')
    
    for _ in range(20):  # 20 seconds timeout
        if wifi.isconnected():
            print("WiFi Connected:", wifi.ifconfig())
            return True
        time.sleep(1)
    
    print("WiFi connection failed!")
    return False

def message_callback(topic, msg):
    try:
        topic_str = topic.decode()
        msg_str = msg.decode()
        
        if topic_str == LED_TOPIC:
            print(f"Received LED1 command: {msg_str}")
            if msg_str.lower() == "on":
                onboard_led.value(1)
            elif msg_str.lower() == "off":
                onboard_led.value(0)
            else:
                print("Unknown LED1 command")

        elif topic_str == LED_TOPIC2:
            print(f"Received LED2 command: {msg_str}")
            if msg_str.lower() == "on":
                onboard_led2.value(1)
            elif msg_str.lower() == "off":
                onboard_led2.value(0)
            else:
                print("Unknown LED2 command")

    except Exception as e:
        print(f"Message Callback Error: {e}")

def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=1883)
    client.set_callback(message_callback)
    client.connect()
    
    client.subscribe(LED_TOPIC)
    client.subscribe(LED_TOPIC2)
    print(f"Connected to MQTT broker {MQTT_BROKER}")
    print(f"Subscribed to topics: {LED_TOPIC}, {LED_TOPIC2}")
    return client

def measure_distance():
    try:
        trigger.off()
        time.sleep_us(2) #I am ensuring that trigger is off initially
        trigger.on()
        time.sleep_us(10)
        trigger.off()##sending a 10us high pulse
        duration=time_pulse_us(echo,1,30000)
        ##measured how long the echo pin remained high
        distance=(duration/2)/29.1
        return round(distance,2)
    except Exception as e:
        return -1

def read_and_publish(client):
    try:
        motion=pir_sensor.value()
        d=measure_distance()

        reading = {
             "motion":"Obstacle" if motion else "Clear",
            "timestamp": time.time()
        }
        client.publish(IR_TOPIC, ujson.dumps(reading))
        print(f"Published to {IR_TOPIC}: {reading}")
        
        distance_reading = {
            "distance": "very close" if d<THRESHOLD else "safe distance",
            "timestamp": time.time()
        }
        client.publish(ULTRASONIC_TOPIC, ujson.dumps(distance_reading))
        print(f"Published to {ULTRASONIC_TOPIC}: {distance_reading}")
        
    except Exception as e:
        print(f"DHT/PIR Read or Publish Error: {e}")

def main():
    if not connect_wifi():
        return
    
    try:
        mqtt_client = connect_mqtt()
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")
        return
    
    while True:
        try:
            mqtt_client.check_msg() 
            read_and_publish(mqtt_client)
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(1)

if __name__ == "__main__": 
    main()