from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'sen0311_driver'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools', 'requests'],
    zip_safe=True,
    maintainer='Gaël Écorchard',
    maintainer_email='gael@km-robotics.cz',
    description='ROS2 node for SEN0311 distance sensor over HTTP (ESPHome)',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sen0311_node = sen0311_driver.sen0311_node:main',
        ],
    },
)
