from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy

def main(args=None):
    rclpy.init(args=args)
    navigator_node = BasicNavigator()
    init_pose = PoseStamped()
    init_pose.header.frame_id = "map"
    init_pose.header.stamp = navigator_node.get_clock().now().to_msg()
    init_pose.pose.position.x = 0.0
    init_pose.pose.position.y = 0.0 
    init_pose.pose.orientation.w = 1.0
    navigator_node.setInitialPose(init_pose)
    navigator_node.waitUntilNav2Active()#wait for nav2 to be ready
    rclpy.spin(navigator_node)
    rclpy.shutdown()        
