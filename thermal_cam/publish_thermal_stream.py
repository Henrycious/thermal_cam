#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np


class ThermalPublisher(Node):
    def __init__(self):
        super().__init__('thermal_publisher')
        self.publisher_ = self.create_publisher(Image,'thermal_stream',10)
        self.publisher2_ = self.create_publisher(Image,'thermal_colormap',10)
        timer_period = 1/60; #camera runs with 60 FPS
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.cam_found = False
        if not self.cam_found:
            for i in range(20):
                self.cap = cv2.VideoCapture(i)
                success, img = self.cap.read()
                if success: 
                    height, width = img.shape[:2]
                    if height == 384 and width == 256:
                        self.cam_found = True           
                        self.vid_channel=i
                        break
                    else:
                        continue
                else:
                    continue
            
        self.cvBridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        colormap = plt.get_cmap('inferno')
        top_frame = frame[0:192,0:256]
        heatmap = cv2.applyColorMap(top_frame, cv2.COLORMAP_JET)


        if ret:
            self.publisher_.publish(self.cvBridge.cv2_to_imgmsg(top_frame))
            self.publisher2_.publish(self.cvBridge.cv2_to_imgmsg(heatmap, encoding='bgr8'))
        
      

        # cv2.imshow("camera", top_frame)
        # cv2.imshow("heatmap", heatmap)
        # cv2.waitKey(1)

def main(args=None):
    
    rclpy.init(args=args)

    thermal_publisher = ThermalPublisher()

    rclpy.spin(thermal_publisher)

    thermal_publisher.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main() 

        
