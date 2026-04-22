from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy

def main(args=None):
    rclpy.init(args=args)
    navigator_node = BasicNavigator()
    #wait navigators to be ready
    navigator_node.waitUntilNav2Active()
    #set goal
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.header.stamp = navigator_node.get_clock().now().to_msg()
    goal_pose.pose.position.x = 2.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 1.0
    navigator_node.goToPose(goal_pose)

    while not navigator_node.isTaskComplete():
        feedback = navigator_node.getFeedback()
        navigator_node.get_logger().info(f"Feedback rest distance: {feedback.distance_remaining:.2f} m")
        #navigator_node.cancelTasks() #cancel tasks if needed
    result = navigator_node.getResult()
    navigator_node.get_logger().info(f"Result: {result.result}")
    #spin
    rclpy.spin(navigator_node)
    #shutdown
    # rclpy.spin(navigator_node)
    # rclpy.shutdown()        
