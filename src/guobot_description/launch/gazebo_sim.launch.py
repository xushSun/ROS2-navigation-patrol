import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    robot_name = "Guobot"
    #获取默认路径：
    package_path = get_package_share_directory('demo_cpp_slam')
    default_urdf_path = os.path.join(package_path,'urdf','Guobot','Guobot.urdf.xacro')
    default_world_model_path = os.path.join(package_path,'world','custom_room.world')
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
    #包含launch文件
    launch_gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('gazebo_ros'),'/launch','/gazebo.launch.py']),
        #传递参数
        launch_arguments=[('world',default_world_model_path),('verbose','true')]
    )
    #状态发布节点
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description' : robot_description}]
    )
    #发布节点
    spawn_entity_node = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic','/robot_description',
                    '-entity',robot_name, ])
    #激活关节控制器
    load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd = ['ros2','control','load_controller','--set-state','active','Guobot_joint_state_broadcaster'],
        output = 'screen'
    )
    #激活力控制器
    load_effort_controller = launch.actions.ExecuteProcess(
        cmd = ['ros2','control','load_controller','--set-state','active','Guobot_effort_controller'],
        output = 'screen'
    )
    #激活速度控制器
    load_diff_drive_controller = launch.actions.ExecuteProcess(
        cmd = ['ros2','control','load_controller','--set-state','active','Guobot_diff_drive_controller'],
        output = 'screen'
    )

    return launch.LaunchDescription([
        action_declare_arg_urdf_path,
        robot_state_publisher_node,
        launch_gazebo,
        spawn_entity_node,
        #事件动作，加载机器人模型后执行
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action = spawn_entity_node,
                on_exit = [load_joint_state_controller],
            )
        ),
        #事件动作，load joint_state_broadcaster后执行
        # launch.actions.RegisterEventHandler(
        #     event_handler=launch.event_handlers.OnProcessExit(
        #         target_action = load_joint_state_controller,
        #         on_exit = [load_effort_controller],
        #     )
        # ),
        #事件动作，load joint_state_broadcaster后执行
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action = load_joint_state_controller,
                on_exit = [load_diff_drive_controller],
            )
        )
    ])