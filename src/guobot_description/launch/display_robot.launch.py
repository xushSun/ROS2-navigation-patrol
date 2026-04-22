import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    #获取默认路径：
    package_path = get_package_share_directory('demo_cpp_slam')
    default_urdf_path = os.path.join(package_path,'urdf','first_robot.urdf')
    robot_model_path = os.path.join(package_path,'config','robot_model.rviz')
    #为launch文件声明参数urdf的路径
    action_declare_arg_urdf_path = launch.actions.DeclareLaunchArgument(
        name='model',default_value=default_urdf_path,
        description='urdf绝对路径'
    )
    #获取文件内容生成新的参数
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(
            ['xacro ',launch.substitutions.LaunchConfiguration('model')],
        ),
        value_type = str
    )
    #状态发布节点
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description' : robot_description}]
    )
    #关节状态发布节点
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher'
    )
    #RVIZ节点
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d',robot_model_path]
    )
    return launch.LaunchDescription([
        action_declare_arg_urdf_path,
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])