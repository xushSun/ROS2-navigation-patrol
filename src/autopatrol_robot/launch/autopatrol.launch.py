import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
import launch_ros
import launch

def generate_launch_description():
    autopatrol_robot_dir = get_package_share_directory('autopatrol_robot')
    config_path = os.path.join(autopatrol_robot_dir, 'config', 'patrol_node.yaml')

    action_node_robot_control = launch_ros.actions.Node(
        package='autopatrol_robot',
        executable='patrol_node',
        output='screen',
        parameters=[config_path]
    )
    action_node_speaker = launch_ros.actions.Node(
        package='autopatrol_robot',
        executable='speaker',
        output='screen'
    )
    return LaunchDescription([
        action_node_speaker,
        action_node_robot_control
        
    ])
        