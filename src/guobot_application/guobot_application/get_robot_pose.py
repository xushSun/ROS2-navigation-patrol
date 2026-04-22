import math
import rclpy
from rclpy.node import Node
import rclpy.time
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformListener, Buffer
from tf_transformations import euler_from_quaternion

class GetRobotPose(Node):
    def __init__(self):
        super().__init__('get_robot_pose')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.get_robot_pose)
    
    def get_robot_pose(self):
        try:
            result = self.tf_buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time(seconds=0.0),rclpy.time.Duration(seconds=1.0))
            transform = result.transform
            self.get_logger().info(f'平移:{transform.translation}')
            self.get_logger().info(f'旋转:{transform.rotation}')
            rotation_euler = euler_from_quaternion([transform.rotation.x, transform.rotation.y, transform.rotation.z, transform.rotation.w]) 
            self.get_logger().info(f'欧拉角:{rotation_euler}')
        except Exception as e:
            self.get_logger().warn('Error getting robot pose: {}'.format(e))

def main():
    rclpy.init()
    node = GetRobotPose()
    rclpy.spin(node)
    rclpy.shutdown()