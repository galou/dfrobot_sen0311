# SEN0311 (Ultrasonic) Sensor Node

This directory contains the ESPHome configuration for the DFRobot SEN0311 Ultrasonic distance sensor (uses `a02yyuw` platform).

## ROS 2 Node
The corresponding ROS 2 node for this sensor is `sen0311_node`. It polls the ESPHome web server to retrieve distance measurements and publishes them as a `sensor_msgs/Range` message.

- **ESPHome Endpoint:** `/sensor/distance`
- **Output Topic:** `/sen0311/Distance` (Range in meters)
- **Frame ID:** `sen0311_link`

### Usage
Run the node using:
```bash
colcon build
source install/setup.bash
ros2 run sen0311_node sen0311_driver --ros-args -p sensor_ip:="192.168.40.20"
```
# Setup instruction
1. (Reccomended, not necesary) Connect the M5 Atom Lite to a pc and flash it with the factory firmware
2. Go to 'web.esphome.io', and connect to your desired wifi network. Check the device ip and modify 'firmware/atomlite-distance.yaml' and  'ros_node\sen0311_driver\sen0311_node.py' to reflect this
3. Compile and run the firmware using pixi 
'pixi run compile'
'pixi run upload --device {ip_address}'
4. Verify that the device runs properly, either by checking the web server, endpoint or ros node (if something isn't working, i reccommend debuging in this order)

# Wiring
- For wiring instructions see 'https://docs.m5stack.com/en/core/Atom-Lite' and 'https://wiki.dfrobot.com/sen0311/#tech_specs'
    
    sensor -> jumper cable -> cable m5

    black -> brown -> black
    red -> red -> red
    blue -> yellow -> yellow
    green ->white -> white

    cable : 'https://docs.m5stack.com/en/accessory/cable/grove_cable'
