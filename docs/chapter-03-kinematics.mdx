---
title: Chapter 3 - Kinematics of Humanoid Robots
sidebar_position: 3
---

# Kinematics of Humanoid Robots

## Theory

Kinematics is the study of motion without considering the forces that cause the motion. In humanoid robotics, kinematics is crucial for understanding how joints and limbs move in space and how to control these movements to achieve desired positions and trajectories.

### Forward Kinematics

Forward kinematics calculates the position and orientation of the end effector (e.g., hand, foot) based on the joint angles throughout the kinematic chain. This is essential for:
- Understanding where robot parts are in space
- Verifying that movements are physically possible
- Simulating robot behavior before execution

### Inverse Kinematics

Inverse kinematics (IK) determines the required joint angles to achieve a desired end effector position and orientation. This is critical for:
- Reaching for objects at specific locations
- Maintaining balance by adjusting foot positions
- Planning natural-looking movements
- Coordinating multiple limbs simultaneously

### Kinematic Chains in Humanoid Robots

Humanoid robots have multiple interconnected kinematic chains:

1. **Left Arm Chain**: Shoulder → Elbow → Wrist
2. **Right Arm Chain**: Shoulder → Elbow → Wrist  
3. **Left Leg Chain**: Hip → Knee → Ankle
4. **Right Leg Chain**: Hip → Knee → Ankle
5. **Head Chain**: Neck joints for orientation
6. **Torso Chain**: Trunk movements

### Degrees of Freedom (DOF)

Each joint in a humanoid robot has one or more degrees of freedom:
- **Revolute joints**: One rotational DOF
- **Prismatic joints**: One translational DOF
- **Spherical joints**: Three rotational DOFs
- **Ball joints**: Three rotational DOFs

A typical humanoid robot has 20-40 DOFs distributed across its body.

### Jacobian Matrix

The Jacobian matrix relates joint velocities to end-effector velocities. It's crucial for:
- Motion planning and control
- Singularity detection and avoidance
- Force control and impedance control
- Redundancy resolution in overactuated systems

### Humanoid-Specific Kinematic Considerations

1. **Balance**: Leg kinematics must ensure the robot's center of mass remains stable
2. **Reachability**: Arm kinematics must enable interaction with objects in human environments
3. **Anthropomorphism**: Joint ranges should match human-like capabilities
4. **Redundancy**: More DOFs than required for specific tasks enables multiple solutions

## Code

```python
import numpy as np
from scipy.spatial.transform import Rotation as R
import math

class HumanoidKinematics:
    def __init__(self):
        # Define humanoid structure (simplified)
        # Using Denavit-Hartenberg parameters for simplicity
        self.links = {
            'left_arm': {
                'upper_arm': 0.3,    # Upper arm length (m)
                'forearm': 0.25,     # Forearm length (m)
                'joint_limits': [
                    (-np.pi/2, np.pi/2),   # Shoulder abduction
                    (-np.pi, 0),           # Shoulder flexion
                    (-np.pi/2, np.pi/2)    # Elbow flexion
                ]
            },
            'right_arm': {
                'upper_arm': 0.3,
                'forearm': 0.25,
                'joint_limits': [
                    (-np.pi/2, np.pi/2),   # Shoulder abduction
                    (-np.pi, 0),           # Shoulder flexion
                    (-np.pi/2, np.pi/2)    # Elbow flexion
                ]
            },
            'left_leg': {
                'thigh': 0.4,        # Thigh length (m)
                'shin': 0.4,         # Shin length (m)
                'joint_limits': [
                    (-np.pi/6, np.pi/6),   # Hip abduction
                    (-np.pi/4, np.pi/2),   # Hip flexion
                    (0, np.pi/2)           # Knee flexion
                ]
            },
            'right_leg': {
                'thigh': 0.4,
                'shin': 0.4,
                'joint_limits': [
                    (-np.pi/6, np.pi/6),   # Hip abduction
                    (-np.pi/4, np.pi/2),   # Hip flexion
                    (0, np.pi/2)           # Knee flexion
                ]
            }
        }

    def dh_transform(self, a, alpha, d, theta):
        """Calculate Denavit-Hartenberg transformation matrix"""
        return np.array([
            [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
            [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1]
        ])

    def forward_kinematics_arm(self, joint_angles, arm_type='left'):
        """Calculate forward kinematics for a 3-DOF arm"""
        if arm_type not in ['left', 'right']:
            raise ValueError("Arm type must be 'left' or 'right'")
        
        a1 = self.links[f'{arm_type}_arm']['upper_arm']
        a2 = self.links[f'{arm_type}_arm']['forearm']
        
        # Simplified model: 3DOF arm (shoulder abduction, shoulder flexion, elbow flexion)
        theta1, theta2, theta3 = joint_angles
        
        # Calculate end effector position
        x = a2 * math.cos(theta2 + theta3) + a1 * math.cos(theta2)
        y = 0  # Simplified - no side movement
        z = a2 * math.sin(theta2 + theta3) + a1 * math.sin(theta2)
        
        # For a complete implementation, we would also calculate orientation
        # This is a 2D planar simplification
        
        return np.array([x, y, z])

    def inverse_kinematics_arm(self, target_pos, arm_type='left', elbow_up=True):
        """Calculate inverse kinematics for a 3-DOF arm"""
        if arm_type not in ['left', 'right']:
            raise ValueError("Arm type must be 'left' or 'right'")
        
        a1 = self.links[f'{arm_type}_arm']['upper_arm']
        a2 = self.links[f'{arm_type}_arm']['forearm']
        
        x, y, z = target_pos
        
        # 2D planar inverse kinematics
        # Calculate distance to target from shoulder
        d = math.sqrt(x**2 + z**2)
        
        if d > a1 + a2:
            raise ValueError("Target position is out of reach")
        
        # Calculate elbow angle using law of cosines
        cos_elbow = (a1**2 + a2**2 - d**2) / (2 * a1 * a2)
        cos_elbow = np.clip(cos_elbow, -1, 1)  # Clamp to avoid numerical errors
        elbow_angle = math.acos(cos_elbow)
        
        # Calculate shoulder angles
        k1 = a1 + a2 * math.cos(elbow_angle)
        k2 = a2 * math.sin(elbow_angle)
        
        alpha = math.atan2(z, x)
        beta = math.atan2(k2, k1)
        
        shoulder_azimuth = alpha - beta
        shoulder_elevation = 0  # Simplified to 2D
        
        # Determine elbow configuration
        if elbow_up:
            elbow_flexion = np.pi - elbow_angle
            shoulder_flexion = shoulder_azimuth
        else:
            elbow_flexion = -(np.pi - elbow_angle)
            shoulder_flexion = shoulder_azimuth
        
        return np.array([shoulder_elevation, shoulder_flexion, elbow_flexion])

    def jacobian_arm(self, joint_angles, arm_type='left'):
        """Calculate Jacobian matrix for 3-DOF arm (simplified 2D version)"""
        if arm_type not in ['left', 'right']:
            raise ValueError("Arm type must be 'left' or 'right'")
        
        a1 = self.links[f'{arm_type}_arm']['upper_arm']
        a2 = self.links[f'{arm_type}_arm']['forearm']
        
        theta1, theta2, theta3 = joint_angles
        
        # Calculate Jacobian elements (simplified 2D)
        J = np.zeros((3, 3))
        
        # Linear velocity part
        J[0, 1] = -a1 * math.sin(theta2) - a2 * math.sin(theta2 + theta3)
        J[0, 2] = -a2 * math.sin(theta2 + theta3)
        J[2, 1] = a1 * math.cos(theta2) + a2 * math.cos(theta2 + theta3)
        J[2, 2] = a2 * math.cos(theta2 + theta3)
        
        # The actual implementation would include orientation
        # and handle full 3D transformations
        
        return J

    def check_joint_limits(self, joint_angles, chain_type, side):
        """Check if joint angles are within limits"""
        chain_key = f'{side}_{chain_type}'
        if chain_key not in self.links:
            raise ValueError(f"Unknown chain: {chain_key}")
        
        limits = self.links[chain_key]['joint_limits']
        
        for i, angle in enumerate(joint_angles):
            if i < len(limits):
                min_limit, max_limit = limits[i]
                if not (min_limit <= angle <= max_limit):
                    return False, f"Joint {i} exceeds limits: {angle:.3f} not in [{min_limit:.3f}, {max_limit:.3f}]"
        
        return True, "All joints within limits"

# Example usage
if __name__ == "__main__":
    kin = HumanoidKinematics()
    
    print("Humanoid Kinematics Example")
    print("=" * 30)
    
    # Example: Move left arm to a position
    target_pos = np.array([0.4, 0.0, 0.1])  # x, y, z in meters
    print(f"Target position: {target_pos}")
    
    try:
        # Calculate required joint angles
        joint_angles = kin.inverse_kinematics_arm(target_pos, 'left')
        print(f"Required joint angles: {joint_angles}")
        
        # Verify with forward kinematics
        calculated_pos = kin.forward_kinematics_arm(joint_angles, 'left')
        print(f"Forward kinematics result: {calculated_pos}")
        print(f"Position error: {np.linalg.norm(target_pos - calculated_pos):.4f}m")
        
        # Check joint limits
        in_limits, msg = kin.check_joint_limits(joint_angles, 'arm', 'left')
        print(f"Joint limits check: {msg}")
        
    except ValueError as e:
        print(f"IK Error: {e}")
    
    print("\n" + "=" * 30)
    
    # Example: Jacobian calculation
    test_angles = np.array([0.0, 0.5, 0.3])  # Some test angles
    J = kin.jacobian_arm(test_angles, 'right')
    print(f"Jacobian matrix for right arm:\n{J}")
```

## Simulation

### Kinematic Simulation in Gazebo

Kinematic models in simulation need to accurately reflect the real-world physical constraints of the robot. Here's how to set up kinematic simulation:

1. **URDF Model Setup**: Define kinematic chains with proper joint limits in your URDF
2. **Kinematic Solvers**: Use KDL or other kinematic libraries with Gazebo
3. **Visualization**: Use RViz2 to visualize planned vs. actual movements
4. **Validation**: Compare simulated kinematics with real robot behavior

### Example ROS 2 Launch for Kinematic Simulation

```xml
<!-- launch/kinematic_demo.launch.xml -->
<launch>
  <!-- Start Gazebo with humanoid model -->
  <include file="$(find-pkg-share my_humanoid_gazebo)/launch/my_humanoid_world.launch.py"/>
  
  <!-- Start robot state publisher -->
  <node pkg="robot_state_publisher" exec="robot_state_publisher" name="robot_state_publisher">
    <param name="robot_description" value="$(var robot_description)"/>
  </node>
  
  <!-- Start joint state publisher (for simulation) -->
  <node pkg="joint_state_publisher" exec="joint_state_publisher" name="joint_state_publisher">
    <param name="use_gui" value="true"/>
  </node>
  
  <!-- Start kinematic controller -->
  <node pkg="my_humanoid_control" exec="kinematic_controller" name="kinematic_controller"/>
  
  <!-- Start RViz2 for visualization -->
  <node pkg="rviz2" exec="rviz2" name="rviz2" args="-d $(find-pkg-share my_humanoid_description)/rviz/kinematics.rviz"/>
</launch>
```

### Simulation Exercises

1. **Forward Kinematics Verification**: 
   - Set known joint angles and verify end-effector position in simulation
   - Compare with analytical calculations

2. **Inverse Kinematics Challenges**:
   - Set various target positions for arms and legs
   - Validate that the robot can reach the positions

3. **Singularity Detection**:
   - Identify positions where the Jacobian becomes singular
   - Visualize the robot configuration in these positions

4. **Workspace Analysis**:
   - Map out the reachable workspace for each limb
   - Identify areas of high dexterity vs. low dexterity

## Exercises

1. **Mathematical Foundations**:
   - Derive the forward kinematics equations for a 6-DOF humanoid arm using DH parameters
   - Calculate the workspace of a 3-DOF leg using geometric methods
   - Prove that the Jacobian of a kinematic chain is the derivative of the forward kinematics function

2. **Implementation Challenges**:
   - Implement the complete 6-DOF inverse kinematics for a humanoid arm using numerical methods
   - Create a kinematic chain visualization tool that shows joint positions in 3D
   - Implement redundancy resolution for a 7-DOF humanoid arm

3. **Simulation Projects**:
   - Create a URDF model of a simplified humanoid with 12 DOF per leg
   - Implement a walking gait using inverse kinematics
   - Simulate the robot reaching for objects at various positions

4. **Advanced Topics**:
   - Implement task-priority kinematics for handling multiple simultaneous objectives
   - Develop a singularity-avoidance algorithm for redundant arms
   - Create a kinematic motion planner that accounts for joint limits

5. **Real-world Application**:
   - Analyze the kinematic properties of a real humanoid robot (e.g., HRP-4, ATLAS)
   - Compare the kinematic capabilities of different humanoid platforms
   - Research how kinematic constraints affect humanoid robot tasks

## Bibliography & Further Reading

1. Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control*. Pearson Prentice Hall.
2. Siciliano, B., & Khatib, O. (Eds.). (2016). *Springer Handbook of Robotics*. Springer.
3. Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2006). *Robot Modeling and Control*. Wiley.
4. NVIDIA Isaac Gym Documentation: https://docs.nvidia.com/isaac/isaac_gym/index.html
5. ROS MoveIt Documentation: https://moveit.ros.org/documentation/