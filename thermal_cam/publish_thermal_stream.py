#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image
import matplotlib.pyplot as plt
import cv2
import os
import re
import numpy as np
from termcolor import colored
from os import path


class ThermalPublisher(Node):
    def __init__(self):
        super().__init__('thermal_publisher')
        self.publisher_ = self.create_publisher(Image,'thermal_stream',10)
        self.publisher2_ = self.create_publisher(Image,'thermal_colormap',10)
        timer_period = 1/60; #camera runs with 60 FPS
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.cam_num = self.get_camera('USB Camera: USB Camera')
        print(self.cam_num)
        self.cap = cv2.VideoCapture(8)
        self.cvBridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        
        if ret:
            colormap = plt.get_cmap('inferno')
            top_frame = frame[0:192,0:256]
            heatmap = cv2.applyColorMap(top_frame, cv2.COLORMAP_JET)
            self.publisher_.publish(self.cvBridge.cv2_to_imgmsg(top_frame))
            self.publisher2_.publish(self.cvBridge.cv2_to_imgmsg(heatmap, encoding='bgr8'))


    def get_camera(self, camera_name):
        cam_num = None
        for file in os.listdir("/sys/class/video4linux"):
            if not path.exists("/sys/class/video4linux/" + file + "/device/input/"):
                continue
            input_name = os.listdir("/sys/class/video4linux/" + file + "/device/input/")
            real_file = os.path.join("/sys/class/video4linux/" + file + "/device/input/"+ input_name[0] + "/name")
            with open(real_file, "rt") as name_file:
                name = name_file.read().rstrip()
            if camera_name in name:
                port_return = file[-1]
                return port_return
                break
            else:
                found = ""

def main(args=None):
    
    rclpy.init(args=args)

    thermal_publisher = ThermalPublisher()

    rclpy.spin(thermal_publisher)

    thermal_publisher.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main() 

        
