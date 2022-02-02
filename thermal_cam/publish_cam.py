#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

class VideoPublisher(Node):
    def __init__(self):
        super().__init__('video_publisher')
        self.publisher_ = self.create_publisher(Image,'/Webcam',10)
        timer_period = 1/60; #camera runs with 60 FPS
        self.timer = self.create_timer(timer_period, self.timer_callback)
       
  
    
        self.cap = cv2.VideoCapture(2)
        success, img = self.cap.read()
   
            
        self.cvBridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        msg = self.cvBridge.cv2_to_imgmsg(frame)

        
        msg.header.frame_id = '1'

        if ret:
            self.publisher_.publish(msg)
      
            self.get_logger().info('Publishing Video frame!')
        


def main(args=None):
    
    rclpy.init(args=args)

    video_publisher = VideoPublisher()

    rclpy.spin(video_publisher)

    video_publisher.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main() 

        
