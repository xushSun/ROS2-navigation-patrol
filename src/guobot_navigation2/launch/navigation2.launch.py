import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    #获取路径
    Guobot_navigation2_dir = get_package_share_directory('guobot_navigation2')
    nav2_bringip_dir = get_package_share_directory('nav2_bringup')
    rviz_config_dir = os.path.join(nav2_bringip_dir, 'rviz', 'nav2_default_view.rviz')
    #创建launch配置
    use_sim_time = launch.substitutions.LaunchConfiguration('use_sim_time', default='true')
    map_yaml_path = launch.substitutions.LaunchConfiguration('map', default=os.path.join(Guobot_navigation2_dir, 'maps', 'room.yaml'))
    nav2_params_path = launch.substitutions.LaunchConfiguration('nav2_param_paths', default=os.path.join(Guobot_navigation2_dir, 'config', 'nav2_params.yaml'))

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='use_sim_time',
            default_value=use_sim_time,
            description='Use simulation (Gazebo) clock if true'),
        launch.actions.DeclareLaunchArgument(
            name='map',
            default_value=map_yaml_path,
            description='Full path to map file to load'),
        launch.actions.DeclareLaunchArgument(
            name='nav2_param_paths',
            default_value=nav2_params_path,
            description='Full path to the ROS2 parameters file to use for all launched nodes'),
        launch.actions.IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_bringip_dir, '/launch','/bringup_launch.py']),
            launch_arguments={
                'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_params_path,             
            }.items()
        ),
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}] 
        )
    ])