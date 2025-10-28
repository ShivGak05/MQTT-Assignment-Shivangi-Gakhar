Files Included:
1. diagram.json:circuit layout
2. main.py:main code
3.README.md – Documentation

Topic tree:
<p align="center">
  <img src="./topictree.png" alt="Simulation Screenshot" width="400"/>
</p>

<p style="color:red; font-weight:600;">Broker Commands:</p>
1. <p style="color:green; font weight:600;">Subscribe to sensor data:</p>
mosquitto_sub -h test.mosquitto.org -t "mqtt-demoShivangi/#"

2.<p style="color:green; font weight:600;">Turn on LED associated with PIR sensor:</p>
mosquitto_pub -h test.mosquitto.org -t "mqtt-demoShivangi/led" -m "on"

3.<p style="color:green; font weight:600;">Turn on LED associated with Ultrasonic sensor:</p>
mosquitto_pub -h test.mosquitto.org -t "mqtt-demoShivangi/led2" -m "on"

4.<p style="color:green; font weight:600;">Turn off LED associated with PIR sensor:</p>
mosquitto_pub -h test.mosquitto.org -t "mqtt-demoShivangi/led" -m "off"

5.<p style="color:green; font weight:600;"> Turn off LED associated with Ultrasonic sensor:</p>
mosquitto_pub -h test.mosquitto.org -t "mqtt-demoShivangi/led" -m "off"

<p style="color:red; font weight:600;">Screenshots:</p>
<p align="center">
  <img src="./image1.png" alt="Simulation Screenshot" width="600"/>
</p>
<p align="center">
  <img src="./image2.png" alt="Simulation Screenshot" width="600"/>
</p>
<p align="center">
  <img src="./image3.png" alt="Simulation Screenshot" width="600"/>
</p>
<p align="center">
  <img src="./image4.png" alt="Simulation Screenshot" width="600"/>
</p>

