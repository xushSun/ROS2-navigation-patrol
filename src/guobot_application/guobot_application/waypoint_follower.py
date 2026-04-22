from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy

def main(args=None):
    rclpy.init(args=args)
    navigator_node = BasicNavigator()
    #wait navigators to be ready
    navigator_node.waitUntilNav2Active()
    goal_poses = []
    #set goal
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.header.stamp = navigator_node.get_clock().now().to_msg()
    goal_pose.pose.position.x = 1.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 1.0
    goal_poses.append(goal_pose)

    goal_pose1 = PoseStamped()
    goal_pose1.header.frame_id = "map"
    goal_pose1.header.stamp = navigator_node.get_clock().now().to_msg()
    goal_pose1.pose.position.x = 0.0
    goal_pose1.pose.position.y = 0.0
    goal_pose1.pose.orientation.w = 1.0
    goal_poses.append(goal_pose1)

    goal_pose2 = PoseStamped()
    goal_pose2.header.frame_id = "map"
    goal_pose2.header.stamp = navigator_node.get_clock().now().to_msg()
    goal_pose2.pose.position.x = 1.5
    goal_pose2.pose.position.y = 1.5
    goal_pose2.pose.orientation.w = 1.0
    goal_poses.append(goal_pose2)

    navigator_node.followWaypoints(goal_poses)

    while not navigator_node.isTaskComplete():
        feedback = navigator_node.getFeedback()
        navigator_node.get_logger().info(f"way points: {feedback.current_waypoint}")
        #navigator_node.cancelTasks() #cancel tasks if needed
    result = navigator_node.getResult()
    navigator_node.get_logger().info(f"Result: {result}")
    #spin
    rclpy.spin(navigator_node)
    #shutdown
    # rclpy.spin(navigator_node)
    # rclpy.shutdown()        
