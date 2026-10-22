from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='g05_prii3_move_jetbot',
            executable='draw_number',
            name='draw_number_node',
            output='screen'
        ),
        Node(
            package='g05_prii3_move_jetbot',
            executable='collision',
            name='collision_avoidance_node',
            output='screen'
        )
    ])