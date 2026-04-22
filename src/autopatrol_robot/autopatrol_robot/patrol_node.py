#整体框架
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped,Pose#消息类型
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
#get robot pose
import rclpy.time
from tf2_ros import TransformListener, Buffer#坐标监听器
from tf_transformations import euler_from_quaternion, quaternion_from_euler#转换四元数到欧拉角
from autopatrol_interface.srv import SpeechText#语音播报模块

from sensor_msgs.msg import Image#图像消息类型
from cv_bridge import CvBridge#图像转换模块
import cv2

class PatrolNode(BasicNavigator):
    def __init__(self, node_name):
        super().__init__(node_name)
        #声明参数
        self.declare_parameter('init_point', [0.0,0.0,0.0])
        self.declare_parameter('goal_point', [0.0,0.0,0.0,1.0,1.0,1.57])
        self.init_point = self.get_parameter('init_point').value
        self.goal_point = self.get_parameter('goal_point').value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.get_current_pose)

        self.speech_client = self.create_client(SpeechText, 'speechtext')#语音播报模块初始化
        #订阅与保存图像相关定义
        self.declare_parameter('image_save_path', '/home/gaoguo/ROS2_learn/L07_slam_ws/src/autopatrol_robot/img' )
        self.image_save_path = self.get_parameter('image_save_path').value
        self.bridge = CvBridge()
        self.latest_image = None
        self.subscription_image = self.create_subscription(Image, '/camera_sensor/image_raw', self.image_callback, 10)
        
    def get_pose_by_xyyaw(self,x,y,yaw):#返回Posestamped类型对象
        pose = PoseStamped()#重点是posestamped类型
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        quat = quaternion_from_euler(0,0,yaw)
        pose.pose.orientation.x = quat[0]
        pose.pose.orientation.y = quat[1]
        pose.pose.orientation.z = quat[2]
        pose.pose.orientation.w = quat[3]
        return pose
    def init_robot_pose(self):#初始化机器人位姿
        #从参数获取初始化点 
        init_pose = self.get_pose_by_xyyaw(self.init_point[0],self.init_point[1],self.init_point[2])
        #设置初始位姿
        self.setInitialPose(init_pose)
        self.waitUntilNav2Active()#等待导航系统准备就绪
    def get_target_points(self):#通过参数值获取目标点集合
        target_points = []
        for index in range(len(self.goal_point) // 3):  # 返回int:
            target_point = [self.goal_point[3*index],self.goal_point[3*index+1],self.goal_point[3*index+2]]
            target_points.append(target_point)
            self.get_logger().info(f"目标点{index+1}: x={self.goal_point[3*index]}, y={self.goal_point[3*index+1]}, yaw={self.goal_point[3*index+2]}")
        return target_points
    
    def nav_to_pose(self,target_point):#导航到目标点
        self.goToPose(target_point)
        while not self.isTaskComplete():
            feedback = self.getFeedback()
            self.get_logger().info(f"Feedback rest distance: {feedback.distance_remaining:.2f} m")
            #navigator_node.cancelTasks() #cancel tasks if needed
        result = self.getResult()
        self.get_logger().info(f"Result: {result}")
        
    def get_current_pose(self):#获取当前位姿

        #while rclpy.ok():
            try:
                result = self.tf_buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time(seconds=0.0),rclpy.time.Duration(seconds=1.0))
                transform = result.transform
                rotation_euler = euler_from_quaternion([transform.rotation.x, transform.rotation.y, transform.rotation.z, transform.rotation.w]) 
                self.get_logger().info(f'平移:{transform.translation}')
                self.get_logger().info(f'旋转:{transform.rotation}')
                self.get_logger().info(f'欧拉角:{rotation_euler}')
                return transform
            except Exception as e:
                self.get_logger().warn('Error getting robot pose: {}'.format(e))
    def speech_text(self,text):#语音合成模块
        if not self.speech_client.wait_for_service(timeout_sec=3.0):
            self.get_logger().warn('语音服务未上线，等待中...')
        request = SpeechText.Request()
        request.text = text
        future = self.speech_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            response = future.result()
            self.get_logger().info(f'语音播报：{response}')
        else:
            self.get_logger().warn('语音播报失败')
    def image_callback(self, msg):#图像保存模块
        self.latest_image = msg
    def record_image(self):#图像记录
        if self.latest_image is not None:
            pose = self.get_current_pose()
            cv_image = self.bridge.imgmsg_to_cv2(self.latest_image)
            cv2.imwrite(f"{self.image_save_path}/image_{pose.translation.x:3.2f}_{pose.translation.y:3.2f}.png", cv_image)
def main():
    rclpy.init()
    patrol_node = PatrolNode('patrol_node')
    patrol_node.speech_text("开始巡逻初始化位置")
    patrol_node.init_robot_pose()
    while rclpy.ok():
        points = patrol_node.get_target_points()
        for point in points:
            target_pose = patrol_node.get_pose_by_xyyaw(point[0],point[1],point[2])
            patrol_node.speech_text(f"开始巡逻目标点{points.index(point)+1}")
            patrol_node.nav_to_pose(target_pose)
            patrol_node.speech_text(f"到达目标点{points.index(point)+1}")
            #记录图像
            patrol_node.speech_text(f"到达目标点{point[0]},{point[1]},开始记录图像")
            patrol_node.record_image()
            patrol_node.speech_text(f"已记录图像")
        rclpy.shutdown()


