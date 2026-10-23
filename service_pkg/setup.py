from setuptools import find_packages, setup

package_name = 'service_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tony Adjartey',
    maintainer_email='tony.adjartey@gmail.com',
    description='MXET 400 - Lab 8: Intro to ROS 2 Services',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'multiply_server = service_pkg.multiply_server:main',
            'multiply_client = service_pkg.multiply_client:main',
            'addition_server = service_pkg.addition_server:main',
            'addition_client = service_pkg.addition_client:main',
        ],
    },
)

