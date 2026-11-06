"""
Launch file for the distance sensor node.

The default value of each launch argument is read from `config/sensor_params.yaml`.
`sensor_ip` has no default and must be given, e.g. `sensor_ip:=192.168.1.2`.
"""

import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    config_path = os.path.join(
        get_package_share_directory('sen0311_driver'),
        'config',
        'sensor_params.yaml',
    )
    with open(config_path) as f:
        defaults = yaml.safe_load(f)['/**']['ros__parameters']

    descriptions = {
        'sensor_ip': 'IP address of the ESPHome distance sensor.',
        'sensor_port': 'HTTP port of the ESPHome web server.',
        'endpoint_path': 'Path of the ESPHome distance endpoint.',
        'poll_frequency': 'Polling frequency in Hz.',
        'frame_id': 'Frame ID for sensor_msgs/Range header.',
    }

    # Arguments without a value in the YAML file (e.g. `sensor_ip`) are required.
    arguments = [
        DeclareLaunchArgument(
            name,
            default_value=str(defaults[name]) if name in defaults else None,
            description=description,
        )
        for name, description in descriptions.items()
    ]

    return LaunchDescription([
        *arguments,
        Node(
            package='sen0311_driver',
            executable='sen0311_node',
            name='sen0311_node',
            output='screen',
            parameters=[{name: LaunchConfiguration(name) for name in descriptions}],
        ),
    ])
