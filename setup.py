from setuptools import setup

package_name = 'thermal_cam'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='henry',
    maintainer_email='henry.gennet@hs-osnabrueck.de',
    description='Simple Video publisher + subscriber (with imshow) for thermal camera',
    license='Apache Licence 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publish_thermal = thermal_cam.publish_thermal_stream:main',
            'subscribe_thermal = thermal_cam.sub_show_thermal_stream:main',
            'publish_webcam = thermal_cam.publish_cam:main',
        ],
    },
)
