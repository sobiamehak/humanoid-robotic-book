---
title: Chapter 2 - The Robotic Nervous System - ROS 2
sidebar_position: 2
---

# The Robotic Nervous System - ROS 2

## Theory

Robot Operating System 2 (ROS 2) is the backbone of modern robotics development, serving as the "nervous system" that connects all components of a robotic system. Unlike traditional operating systems, ROS 2 is a flexible framework for writing robot software that handles communication, coordination, and resource management across diverse robot platforms.

### Why ROS 2 is Essential for Physical AI

ROS 2 provides critical infrastructure for Physical AI systems:

1. **Communication Layer**: Enables reliable message passing between different robot components (sensors, processors, actuators)
2. **Hardware Abstraction**: Provides consistent interfaces across different hardware platforms
3. **Tool Ecosystem**: Comprehensive tools for debugging, visualization, and simulation
4. **Package Management**: Standardized way to distribute and reuse robot software
5. **Real-time Capabilities**: Support for time-sensitive operations crucial in Physical AI
6. **Multi-Robot Support**: Coordination between multiple robots in shared environments
7. **Security Features**: Authentication, authorization, and encryption for safe robot operation

### Key Architectural Changes from ROS 1 to ROS 2

ROS 2 addresses critical limitations of ROS 1:

- **Middleware Independence**: Uses DDS (Data Distribution Service) enabling better real-time performance
- **Quality of Service (QoS)**: Configurable reliability and performance settings for message passing
- **Security**: Built-in security with authentication, access control, and encryption
- **Multi-platform Support**: Robust support across operating systems and architectures
- **Lifecycle Management**: Better management of node states and system startup/shutdown
- **Real-time Support**: Better real-time performance with deterministic behavior

### Core ROS 2 Concepts

#### Nodes
Nodes are processes that perform computation. In a humanoid robot, you might have:
- Sensor driver nodes (camera, IMU, LIDAR)
- Processing nodes (perception, decision making)
- Controller nodes (motor control, balance control)
- Interface nodes (visualization, teleoperation)

#### Topics
Topics provide asynchronous communication using a publish/subscribe model. Examples in humanoid robots:
- `/joint_states`: Current positions of all joints
- `/camera/image_raw`: Raw image data from cameras
- `/cmd_vel`: Velocity commands for navigation
- `/tf`: Coordinate transforms between robot parts

#### Services
Services provide synchronous request/response communication. Used for:
- Calibration procedures
- Configuration changes
- Emergency stop commands
- Map saving/loading

#### Actions
Actions provide asynchronous request/response with feedback and status updates. Ideal for:
- Navigation goals
- Manipulation tasks
- Calibration procedures that take time

### ROS 2 for Humanoid Robotics Architecture

In humanoid robotics, ROS 2 typically implements a layered architecture:

1. **Hardware Layer**: Direct communication with sensors and actuators
2. **Driver Layer**: Hardware abstraction and control interfaces
3. **State Estimation**: Sensor fusion and state estimation (position, orientation, joint states)
4. **Perception**: Object recognition, scene understanding, affordance detection
5. **Planning**: Path planning, motion planning, high-level task planning
6. **Control**: Motion control, balance, coordination
7. **Behavior**: High-level robot behaviors and skills
8. **Interface**: User interaction, teleoperation, visualization

## Code

```python
#!/usr/bin/env python3
# Example ROS 2 node for humanoid robot joint control

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray
import numpy as np

class HumanoidJointController(Node):
    def __init__(self):
        super().__init__('humanoid_joint_controller')
        
        # Subscribe to joint state commands
        self.joint_cmd_sub = self.create_subscription(
            Float64MultiArray,
            '/humanoid/joint_commands',
            self.joint_command_callback,
            10
        )
        
        # Subscribe to velocity commands
        self.vel_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.velocity_command_callback,
            10
        )
        
        # Publish actual joint states
        self.joint_pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )
        
        # Timer for publishing joint states
        self.timer = self.create_timer(0.05, self.publish_joint_states)  # 20Hz update
        
        # Initialize joint positions (in radians)
        self.joint_names = [
            'left_hip', 'left_knee', 'left_ankle', 
            'right_hip', 'right_knee', 'right_ankle',
            'left_shoulder', 'left_elbow', 'left_wrist',
            'right_shoulder', 'right_elbow', 'right_wrist',
            'neck_yaw', 'neck_pitch'
        ]
        
        self.joint_positions = [0.0] * len(self.joint_names)
        self.joint_velocities = [0.0] * len(self.joint_names)
        self.joint_efforts = [0.0] * len(self.joint_names)
        
        self.get_logger().info('Humanoid Joint Controller initialized')

    def joint_command_callback(self, msg):
        """Process joint position commands"""
        if len(msg.data) == len(self.joint_names):
            # Simple position control (in a real robot, this would go to hardware)
            self.joint_positions = list(msg.data)
            self.get_logger().debug(f'Joint positions updated: {self.joint_positions[:3]}...')
        else:
            self.get_logger().error(f'Invalid command length: got {len(msg.data)}, expected {len(self.joint_names)}')

    def velocity_command_callback(self, msg):
        """Process velocity commands"""
        linear_x = msg.linear.x
        linear_y = msg.linear.y
        angular_z = msg.angular.z
        
        self.get_logger().info(f'Received velocity command: v_x={linear_x:.2f}, v_y={linear_y:.2f}, ω={angular_z:.2f}')
        
        # In a real humanoid, this would trigger walking pattern generators
        if abs(linear_x) > 0.01 or abs(linear_y) > 0.01 or abs(angular_z) > 0.01:
            self.execute_locomotion_command(linear_x, linear_y, angular_z)

    def execute_locomotion_command(self, linear_x, linear_y, angular_z):
        """Execute locomotion based on velocity commands"""
        # This would implement walking pattern generation in a real robot
        self.get_logger().info('Generating walking pattern...')
        
        # Placeholder: make slight adjustments to joint positions to simulate walking
        # In reality, this would involve complex balance control and gait generation
        
    def publish_joint_states(self):
        """Publish current joint states"""
        msg = JointState()
        msg.name = self.joint_names
        msg.position = self.joint_positions
        msg.velocity = self.joint_velocities
        msg.effort = self.joint_efforts
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        self.joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    
    controller = HumanoidJointController()
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info('Shutting down Humanoid Joint Controller')
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Simulation

### Setting up ROS 2 for Humanoid Simulation

To properly simulate a humanoid robot in ROS 2:

1. **Install ROS 2 Humble Hawksbill**: This is the recommended version for humanoid robotics
2. **Install Gazebo Harmonic**: Compatible with ROS 2 Humble
3. **Install robot simulation packages**:
   ```bash
   sudo apt install ros-humble-gazebo-ros-pkgs
   sudo apt install ros-humble-joint-state-publisher
   sudo apt install ros-humble-robot-state-publisher
   sudo apt install ros-humble-xacro
   ```

### Simulation Launch Example

To launch a humanoid robot simulation:

```bash
# Terminal 1: Launch Gazebo with your robot
ros2 launch my_robot_gazebo my_humanoid_world.launch.py

# Terminal 2: Start the controller
ros2 run my_robot_control humanoid_joint_controller

# Terminal 3: Send commands to the robot
ros2 topic pub /humanoid/joint_commands std_msgs/Float64MultiArray "data: [0.1, -0.2, 0.05, 0.1, -0.2, 0.05, 0.3, -0.5, 0.2, 0.3, -0.5, 0.2, 0.0, 0.0]"
```

### Gazebo Simulation Components

1. **Model Files (.urdf/.sdf)**: Define robot geometry and physics properties
2. **Gazebo Plugins**: ROS 2 interfaces for sensors and actuators
3. **Control Interfaces**: Joint controllers, gripper interfaces, etc.
4. **Launch Files**: Configure and start complete simulation environments

## Exercises

1. **ROS 2 Basics**:
   - Install ROS 2 Humble and create a new workspace
   - Create a publisher node that publishes joint positions for a 12-joint arm
   - Create a subscriber node that prints received messages
   - Use `ros2 run` and `ros2 launch` to control your nodes

2. **Humanoid Control Architecture**:
   - Design a ROS 2 package structure for humanoid robot control
   - Create message definitions for humanoid-specific data types
   - Implement a simple joint trajectory controller using ROS 2 actions
   - Test your controller with a simulated robot

3. **Simulation Integration**:
   - Create a URDF model of a simple humanoid robot (minimum 12 joints)
   - Integrate the robot model with Gazebo physics
   - Implement a walking pattern generator as a ROS 2 node
   - Visualize the robot in RViz2 with joint state feedback

4. **Advanced ROS 2 Features**:
   - Implement QoS policies for different types of messages
   - Create a multi-node system with lifecycle management
   - Add security features (authentication, encryption) to your ROS 2 system
   - Use ROS 2 parameters to configure robot behavior at runtime

5. **Real-world Application**:
   - Research a humanoid robot platform (e.g., NAO, Pepper, HRP-4, ATLAS) and analyze its ROS 2 implementation
   - Create a ROS 2 package that implements a simple manipulation task
   - Document the differences between ROS 1 and ROS 2 approaches for the same task
   - Compare performance between different DDS implementations in ROS 2

## Bibliography & Further Reading

1. Quigley, M., et al. (2009). "ROS: an open-source Robot Operating System." *ICRA Workshop on Open Source Software*.
2. MX. (2021). *Programming Robots with ROS: A Practical Introduction to the Robot Operating System*. O'Reilly Media.
3. ROS 2 Documentation: https://docs.ros.org/en/humble/
4. ROS-Industrial Consortium: https://rosindustrial.org/
5. MIT CSAIL ROS 2 Tutorials: https://github.com/ros2/tutorials