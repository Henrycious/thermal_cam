import rclpy   
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ThermalSubscriber(Node):
    def __init__(self):
        super().__init__('thermal_subscriber')

        self.subscription = self.create_subscription(Image,'thermal_stream',self.listener_callback,10)
        self.subscription

        self.cvBridge = CvBridge()

    def listener_callback(self,data):
        self.get_logger().info('Receiving Thermal Frame')

        current_frame = self.cvBridge.imgmsg_to_cv2(data)
        cv2.imshow("thermal_camera", current_frame)

        cv2.waitKey(1)

def main(args=None):

    rclpy.init(args=args)

    thermal_subscriber = ThermalSubscriber()

    rclpy.spin(thermal_subscriber)

    thermal_subscriber.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()