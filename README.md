# SEN0311 (Ultrasonic) Sensor Node

This directory contains the ESPHome configuration and ROS2 driever for the DFRobot SEN0311 Ultrasonic distance sensor.

## Directory structure
- `firmware/`: Contains the ESPHome configuration (`atomlite-distance.yaml`) and related files for the [Atom Lite board](https://shop.m5stack.com/products/atom-lite-esp32-development-kit) for the SEN0311 sensor(https://wiki.dfrobot.com/sen0311/).

- `ros_node/`: Contains the `sen0311_driver` ROS 2 package to interface with the sensor over HTTP.

## Sensor wiring
- For wiring instructions see the dfrobot wiki( https://wiki.dfrobot.com/sen0311/#tech_specs)

## Build and flash instructions
```bash
pixi run compile
pixi run upload (--device {M5 ip address})
```

## Network configuration

The sensor is configured to use a static IP address (`192.168.40.21`) on a private network. Use `secrets.yaml` to set the network credentials. To switch to a different network, update `secrets.yaml` or use the ESPHome captive portal.

Format of `secrets.yaml`
```yaml
wifi_ssid: "YourWifiSSID"
wifi_password: "YourWifiPassword"
```

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
