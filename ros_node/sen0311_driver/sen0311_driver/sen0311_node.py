#!/usr/bin/env python3

import rclpy
import requests
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import Range


class SEN0311Node(Node):
    """
    ROS node for the SEN0311 ultrasonic distance sensor.

    ROS node for the SEN0311 ultrasonic distance sensor connected to an M5 Atom Lite on
    which ESPHome is running. It polls the sensor over HTTP and publishes the distance as
    a Range message.
    """
    # Sensor parameters, from the datasheet.
    # Cf. https://www.dfrobot.com/product-1935.html
    field_of_view = 1.047  # radians, 60°.
    min_range = 0.030  # meters.
    max_range = 4.5  # meters.

    def __init__(self):
        super().__init__('sen0311_node')

        self.declare_parameter('sensor_ip', Parameter.Type.STRING)
        self.declare_parameter('sensor_port', 80)
        self.declare_parameter('endpoint_path', '/sensor/distance')
        self.declare_parameter('poll_frequency', 20.0)
        self.declare_parameter('frame_id', 'sen0311')

        self.sensor_ip = self.get_parameter('sensor_ip').get_parameter_value().string_value
        self.sensor_port = self.get_parameter('sensor_port').get_parameter_value().integer_value
        if not (0 <= self.sensor_port <= 65535):
            raise ValueError("Parameter `sensor_port` must be in the range [0, 65535]")
        self.endpoint_path = self.get_parameter('endpoint_path').get_parameter_value().string_value
        if not self.endpoint_path.startswith('/'):
            self.get_logger().warn(f"Parameter `endpoint_path` should start with '/'. Prepending '/' to '{self.endpoint_path}'")
            self.endpoint_path = '/' + self.endpoint_path
        self.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        poll_frequency = self.get_parameter('poll_frequency').get_parameter_value().double_value
        if poll_frequency <= 0:
            raise ValueError("Parameter `poll_frequency` must be positive")
        poll_period = 1.0 / poll_frequency

        self.url = f'http://{self.sensor_ip}:{self.sensor_port}{self.endpoint_path}'
        self._session = requests.Session()
        self._publisher = self.create_publisher(Range, '/sen0311/range', 10)
        self._timer = self.create_timer(poll_period, self.timer_callback)

        self.get_logger().info(f'SEN0311 node started: {self.url}')

    def timer_callback(self):
        try:
            response = self._session.get(self.url, timeout=(1.0, 2.0))
            response.raise_for_status()
            data = response.json()
            distance_mm = float(data['value'])
            distance_m = 0.001 * distance_mm

            msg = Range()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self.frame_id
            msg.radiation_type = Range.ULTRASOUND
            msg.field_of_view = self.field_of_view
            msg.min_range = self.min_range
            msg.max_range = self.max_range
            msg.range = distance_m

            self._publisher.publish(msg)
        except Exception as e:
            self.get_logger().warn(f'Error: {e}', throttle_duration_sec=2.0)


def main(args=None):
    rclpy.init(args=args)
    node = SEN0311Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
