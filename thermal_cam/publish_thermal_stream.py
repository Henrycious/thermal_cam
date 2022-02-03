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


class ThermalPublisher(Node):
    def __init__(self):
        super().__init__('thermal_publisher')
        self.publisher_ = self.create_publisher(Image,'thermal_stream',10)
        self.publisher2_ = self.create_publisher(Image,'thermal_colormap',10)
        timer_period = 1/60; #camera runs with 60 FPS
        self.timer = self.create_timer(timer_period, self.timer_callback)

        cam_number = self.get_camera_index_by_name('USB Camera: USB Camera')
        self.cap = cv2.VideoCapture(cam_number)

        self.cvBridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        
        if ret:
            colormap = plt.get_cmap('inferno')
            top_frame = frame[0:192,0:256]
            heatmap = cv2.applyColorMap(top_frame, cv2.COLORMAP_JET)
            self.publisher_.publish(self.cvBridge.cv2_to_imgmsg(top_frame))
            self.publisher2_.publish(self.cvBridge.cv2_to_imgmsg(heatmap, encoding='bgr8'))

    def get_camera_index_by_name(camera_name):
            cam_num = None
            for file in os.listdir("/sys/class/video4linux"):
                real_file = os.path.realpath("/sys/class/video4linux/" + file + "/name")
                with open(real_file, "rt") as name_file:
                    name = name_file.read().rstrip()
                if camera_name in name:
                    cam_num = int(re.search("\d+$", file).group(0))
                    found = "FOUND!"
                    return cam_num
                    break
                else:
                    found = "      "
                print("{} {} -> {}".format(found, file, name))
            return cam_num

def main(args=None):
    
    rclpy.init(args=args)

    thermal_publisher = ThermalPublisher()

    rclpy.spin(thermal_publisher)

    thermal_publisher.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main() 

        
