import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageFlipperNode(Node):
    def __init__(self):
        super().__init__('image_flipper_node')

        # Declare configurable topic parameters
        self.declare_parameter('input_topic', 'camera/image_raw')
        self.declare_parameter('output_topic', 'camera/image_flipped')

        input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        output_topic = self.get_parameter('output_topic').get_parameter_value().string_value

        # Initialize CV Bridge
        self.bridge = CvBridge()

        # Set up Subscriber and Publisher
        self.subscription = self.create_subscription(
            Image,
            input_topic,
            self.image_callback,
            10 # QoS depth
        )
        self.publisher = self.create_publisher(Image, output_topic, 10)

        self.get_logger().info(f"Flipping images from '{input_topic}' -> '{output_topic}'")

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV format
            # Using 'passthrough' keeps the original encoding (e.g., bgr8, mono8)
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            
            # Flip the image
            # 0 = vertical flip, 1 = horizontal flip, -1 = both (180-degree rotation)
            # A camera mounted upside down requires a -1 flip.
            flipped_image = cv2.flip(cv_image, -1)
            
            # Convert back to a ROS Image message
            flipped_msg = self.bridge.cv2_to_imgmsg(flipped_image, encoding=msg.encoding)
            
            # Crucial step: Copy the original header to preserve the exact timestamp
            flipped_msg.header = msg.header
            
            # Publish the result
            self.publisher.publish(flipped_msg)
            
        except Exception as e:
            self.get_logger().error(f'Failed to process image: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ImageFlipperNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
