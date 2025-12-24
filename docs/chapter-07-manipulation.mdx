---
title: Chapter 7 - Manipulation and Grasping
sidebar_position: 7
---

# Manipulation and Grasping

## Theory

Manipulation is a critical capability for humanoid robots to interact with objects in human environments. This involves planning and controlling the robot's arms and hands to grasp, move, and manipulate objects effectively. Unlike simple grippers, humanoid hands must handle a wide variety of objects with different shapes, sizes, and properties while maintaining stability and dexterity.

### Core Manipulation Concepts

#### Degrees of Freedom and Dexterity
- **Arm DOF**: Typically 6-7 DOF per arm (shoulder: 3, elbow: 1, wrist: 2-3)
- **Hand DOF**: 13-20+ DOF for anthropomorphic hands
- **Redundancy**: More DOF than required for basic tasks, enabling multiple solutions
- **Workspace**: Volume where end-effector can be positioned and oriented

#### Grasping Types
- **Power Grasp**: Firm grip using fingers and palm, high force capacity
- **Precision Grasp**: Delicate grip using fingertips, high dexterity
- **Pinch Grasp**: Grasp between thumb and one finger
- **Lateral Grasp**: Grasp with thumb and side of index finger

#### Kinematic Considerations
- **Reachable Workspace**: Volume that can be reached by the end-effector
- **Dexterous Workspace**: Volume where all orientations can be achieved
- **Joint Limits**: Constraints preventing self-collision and damage
- **Singularities**: Configurations where the arm loses mobility

### Grasping Strategies

#### Analytical Grasping
- **Antipodal Grasps**: Opposing forces for stable grasp
- **Force Closure**: Grasp that can resist any external wrench
- **Form Closure**: Grasp that constrains all object motions geometrically
- **Grasp Quality Metrics**: Quantitative measures of grasp stability

#### Data-Driven Grasping
- **Grasp Learning**: Training on large datasets of successful grasps
- **Deep Learning Approaches**: CNNs for grasp planning from images
- **Reinforcement Learning**: Learning grasping policies through trials
- **Human Demonstration**: Learning from human grasping examples

### Manipulation Planning

#### Motion Planning
- **Configuration Space (C-space)**: Space of all possible robot configurations
- **Collision Checking**: Ensuring robot doesn't collide with environment
- **Path Smoothing**: Optimizing paths for execution efficiency
- **Dynamic Constraints**: Considering robot dynamics in motion planning

#### Task Planning
- **Symbolic Planning**: High-level task decomposition
- **Grasp Planning**: Determining optimal grasp configurations
- **Placement Planning**: Where to place objects for tasks
- **Multi-step Sequences**: Planning complex manipulation tasks

### Control Architectures for Manipulation

#### Impedance Control
- **Stiffness Control**: Adjusting apparent stiffness of end-effector
- **Compliance**: Allowing controlled motion under external forces
- **Safety**: Preventing damage from unexpected contacts
- **Human-Robot Interaction**: Safe physical interaction

#### Hybrid Force-Motion Control
- **Constraint Definition**: Defining motion and force constraints
- **Task Coordinates**: Separating force and motion control directions
- **Adaptation**: Adjusting behavior based on contact conditions
- **Assembly Tasks**: Precise control for insertion tasks

### Hand Design Considerations

#### Anthropomorphic Design
- **Human Hand Anatomy**: Mimicking human hand structure and function
- **Underactuation**: Using fewer actuators than DOF for simplicity
- **Tendon Systems**: Transmitting forces through tendons like human muscles
- **Adaptive Mechanisms**: Mechanisms that adapt to object shapes

#### Sensory Integration
- **Tactile Sensing**: Distributed pressure and force sensing
- **Proprioception**: Joint angle and position sensing
- **Slip Detection**: Early detection of object slip
- **Force Sensing**: Measuring grasp forces and object weight

### Grasp Planning Challenges

#### Object Recognition
- **Shape Estimation**: Understanding object geometry
- **Material Properties**: Recognizing object stiffness, fragility
- **Pose Estimation**: Determining object position and orientation
- **Uncertainty Handling**: Dealing with perception uncertainty

#### Grasp Synthesis
- **Pre-shape Planning**: Planning initial hand configuration
- **Adaptive Grasping**: Adjusting grasp based on object properties
- **Multi-finger Coordination**: Coordinating multiple fingers
- **Robustness**: Creating grasps that work despite uncertainty

## Code

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional
from scipy.spatial.transform import Rotation as R
import cvxpy as cp

@dataclass
class Grasp:
    """Represents a grasp configuration"""
    position: np.ndarray  # 3D position of grasp center
    orientation: np.ndarray  # 3D orientation (e.g., quaternion or rotation matrix)
    finger_positions: List[np.ndarray]  # Positions of each finger
    grasp_type: str  # 'power', 'precision', 'pinch', etc.
    quality: float  # Grasp quality metric
    forces: List[np.ndarray]  # Expected contact forces at each finger

@dataclass
class ObjectProperties:
    """Properties of an object to be grasped"""
    shape: str  # 'cylinder', 'box', 'sphere', 'complex'
    dimensions: np.ndarray  # Width, height, depth
    mass: float
    com: np.ndarray  # Center of mass
    friction_coeff: float
    surface_texture: str  # Smooth, rough, etc.

@dataclass
class ManipulationTask:
    """Represents a manipulation task"""
    object_properties: ObjectProperties
    target_pose: np.ndarray  # Target position and orientation for the object
    constraints: List[str]  # Task constraints (e.g., delicate, orientation constraints)
    trajectory: List[np.ndarray]  # Planned trajectory for the end-effector

class HumanoidManipulation:
    def __init__(self, hand_dof=16, arm_dof=7):
        """
        Initialize manipulation system for humanoid robot
        """
        self.hand_dof = hand_dof
        self.arm_dof = arm_dof
        
        # Hand parameters
        self.finger_count = 5  # Assuming anthropomorphic hand
        self.finger_lengths = [0.04, 0.07, 0.06]  # phalanx lengths (thumb, index, middle)
        
        # Robot arm parameters (simplified)
        self.arm_lengths = [0.3, 0.3, 0.1]  # shoulder to elbow, elbow to wrist, wrist to hand
        
        # Grasp quality threshold
        self.grasp_quality_threshold = 0.3
        
    def compute_grasp_candidates(self, object_props: ObjectProperties) -> List[Grasp]:
        """
        Compute potential grasp candidates for an object
        """
        candidates = []
        
        # Generate grasp positions based on object shape and size
        if object_props.shape == 'cylinder':
            candidates = self._generate_cylinder_grasps(object_props)
        elif object_props.shape == 'box':
            candidates = self._generate_box_grasps(object_props)
        elif object_props.shape == 'sphere':
            candidates = self._generate_sphere_grasps(object_props)
        else:
            # For complex shapes, use more general approach
            candidates = self._generate_complex_grasps(object_props)
        
        # Filter by grasp quality
        high_quality_grasps = [g for g in candidates if g.quality > self.grasp_quality_threshold]
        
        return high_quality_grasps
    
    def _generate_cylinder_grasps(self, obj_props: ObjectProperties) -> List[Grasp]:
        """Generate grasps for cylindrical objects"""
        grasps = []
        
        # Dimensions
        radius = obj_props.dimensions[0] / 2
        height = obj_props.dimensions[1]
        
        # Power grasp along the long axis
        pos = obj_props.com.copy()
        pos[2] += height / 2  # Center in the middle of the cylinder
        
        # Approach from different directions
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            # Power grasp: fingers wrap around the cylinder
            grasp_pos = pos.copy()
            
            # Orientation to grasp along the cylindrical axis
            orientation = R.from_euler('xyz', [0, 0, angle]).as_quat()
            
            # Simulated finger positions
            finger_positions = self._compute_finger_positions_cylinder(
                grasp_pos, orientation, radius)
            
            # Calculate grasp quality (simplified)
            quality = self._evaluate_grasp_quality(finger_positions, obj_props)
            
            grasp = Grasp(
                position=grasp_pos,
                orientation=orientation,
                finger_positions=finger_positions,
                grasp_type='power',
                quality=quality,
                forces=[np.zeros(3) for _ in range(len(finger_positions))]  # Placeholder
            )
            
            grasps.append(grasp)
        
        # Precision grasp at the top (pinching)
        for angle in [0, np.pi/2]:
            pos_top = obj_props.com.copy()
            pos_top[2] += height / 2 + 0.02  # Slightly above top
            
            orientation = R.from_euler('xyz', [np.pi/2, 0, angle]).as_quat()
            
            # Simulated thumb and finger positions for pinch grasp
            finger_positions = [
                pos_top + np.array([0, 0.02, 0]),  # Index finger
                pos_top + np.array([0, -0.02, 0])  # Thumb
            ]
            
            quality = self._evaluate_grasp_quality(finger_positions, obj_props, grasp_type='precision')
            
            grasp = Grasp(
                position=pos_top,
                orientation=orientation,
                finger_positions=finger_positions,
                grasp_type='pinch',
                quality=quality,
                forces=[np.zeros(3) for _ in range(len(finger_positions))]
            )
            
            grasps.append(grasp)
        
        return grasps
    
    def _generate_box_grasps(self, obj_props: ObjectProperties) -> List[Grasp]:
        """Generate grasps for box-shaped objects"""
        grasps = []
        
        # Dimensions
        width, height, depth = obj_props.dimensions
        
        # Generate corner grasps for power grasp
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                for dz in [-1, 1]:
                    # Position at corner
                    pos = obj_props.com + np.array([dx * width/2, dy * depth/2, dz * height/2])
                    
                    # Orientation for corner grasp
                    orientation = R.from_euler('xyz', [np.pi/4, 0, 0]).as_quat()
                    
                    # Compute finger positions
                    finger_positions = self._compute_finger_positions_box(
                        pos, orientation, obj_props.dimensions)
                    
                    quality = self._evaluate_grasp_quality(finger_positions, obj_props)
                    
                    grasp = Grasp(
                        position=pos,
                        orientation=orientation,
                        finger_positions=finger_positions,
                        grasp_type='power',
                        quality=quality,
                        forces=[np.zeros(3) for _ in range(len(finger_positions))]
                    )
                    
                    grasps.append(grasp)
        
        # Generate face grasps for precision
        face_configs = [
            # Top face grasps
            (np.array([0, 0, height/2 + 0.02]), [0, 0, 0]),
            # Side face grasps
            (np.array([width/2 + 0.02, 0, 0]), [0, np.pi/2, 0]),
            (np.array([-width/2 - 0.02, 0, 0]), [0, -np.pi/2, 0]),
            (np.array([0, depth/2 + 0.02, 0]), [np.pi/2, 0, 0]),
            (np.array([0, -depth/2 - 0.02, 0]), [-np.pi/2, 0, 0]),
        ]
        
        for pos, euler_angles in face_configs:
            pos = obj_props.com + pos
            orientation = R.from_euler('xyz', euler_angles).as_quat()
            
            # Simulated finger positions for precision grasp
            finger_positions = [
                pos + np.array([0, 0, 0.02]),
                pos + np.array([0, 0, -0.02])
            ]
            
            # Evaluate precision grasp quality
            quality = self._evaluate_grasp_quality(finger_positions, obj_props, grasp_type='precision')
            
            grasp = Grasp(
                position=pos,
                orientation=orientation,
                finger_positions=finger_positions,
                grasp_type='precision',
                quality=quality,
                forces=[np.zeros(3) for _ in range(len(finger_positions))]
            )
            
            grasps.append(grasp)
        
        return grasps
    
    def _generate_sphere_grasps(self, obj_props: ObjectProperties) -> List[Grasp]:
        """Generate grasps for spherical objects"""
        grasps = []
        
        radius = obj_props.dimensions[0] / 2
        
        # Try different approach directions
        for theta in np.linspace(0, np.pi, 4):
            for phi in np.linspace(0, 2*np.pi, 4):
                # Calculate grasp position on sphere surface
                x = obj_props.com[0] + radius * np.sin(theta) * np.cos(phi)
                y = obj_props.com[1] + radius * np.sin(theta) * np.sin(phi)
                z = obj_props.com[2] + radius * np.cos(theta)
                
                grasp_pos = np.array([x, y, z])
                
                # Orientation to be perpendicular to sphere surface
                normal = grasp_pos - obj_props.com
                normal = normal / np.linalg.norm(normal)
                
                # Create orientation where z-axis points toward the sphere center
                z_axis = -normal
                x_axis = np.array([1, 0, 0]) if abs(np.dot(z_axis, [1, 0, 0])) < 0.9 else np.array([0, 1, 0])
                y_axis = np.cross(z_axis, x_axis)
                x_axis = np.cross(y_axis, z_axis)
                
                # Create rotation matrix and convert to quaternion
                rot_matrix = np.column_stack([x_axis, y_axis, z_axis])
                orientation = R.from_matrix(rot_matrix).as_quat()
                
                # Compute finger positions around the sphere
                finger_positions = self._compute_finger_positions_sphere(
                    grasp_pos, orientation, radius)
                
                quality = self._evaluate_grasp_quality(finger_positions, obj_props, grasp_type='spherical')
                
                grasp = Grasp(
                    position=grasp_pos,
                    orientation=orientation,
                    finger_positions=finger_positions,
                    grasp_type='wrap',
                    quality=quality,
                    forces=[np.zeros(3) for _ in range(len(finger_positions))]
                )
                
                grasps.append(grasp)
        
        return grasps
    
    def _generate_complex_grasps(self, obj_props: ObjectProperties) -> List[Grasp]:
        """
        Generate grasps for complex shapes using general approach
        In practice, this would involve more sophisticated methods
        """
        # This is a placeholder - in reality, this would use:
        # - 3D point cloud analysis
        # - Machine learning models
        # - Physics simulation
        
        grasps = []
        
        # For now, just generate grasps at the object's center
        grasp_pos = obj_props.com
        orientation = R.from_euler('xyz', [0, 0, 0]).as_quat()
        
        # Create a simple precision grasp
        finger_positions = [
            grasp_pos + np.array([0.02, 0.0, 0.0]),
            grasp_pos + np.array([-0.02, 0.0, 0.0])
        ]
        
        # Lower quality for unknown shapes
        quality = 0.4
        
        grasp = Grasp(
            position=grasp_pos,
            orientation=orientation,
            finger_positions=finger_positions,
            grasp_type='precision',
            quality=quality,
            forces=[np.zeros(3) for _ in range(len(finger_positions))]
        )
        
        grasps.append(grasp)
        return grasps
    
    def _compute_finger_positions_cylinder(self, grasp_pos, orientation, radius):
        """Compute finger positions for cylinder grasp"""
        # For power grasp on cylinder, fingers wrap around the circumference
        rot_matrix = R.from_quat(orientation).as_matrix()
        
        # Create ring of finger positions around the cylinder
        finger_positions = []
        for i in range(5):  # 5 fingers
            angle = 2 * np.pi * i / 5  # Distribute around the cylinder
            offset = np.array([
                radius * np.cos(angle),
                radius * np.sin(angle),
                0
            ])
            
            # Rotate based on grasp orientation
            offset_rotated = rot_matrix @ offset
            finger_positions.append(grasp_pos + offset_rotated)
        
        return finger_positions
    
    def _compute_finger_positions_box(self, grasp_pos, orientation, dimensions):
        """Compute finger positions for box grasp"""
        rot_matrix = R.from_quat(orientation).as_matrix()
        
        # For box grasp, fingers approach from different sides
        finger_positions = []
        
        # Thumb position
        thumb_offset = np.array([0.03, -0.02, 0])  # Offset to avoid collision
        thumb_pos = grasp_pos + rot_matrix @ thumb_offset
        finger_positions.append(thumb_pos)
        
        # Other fingers (index, middle, ring, little)
        finger_offsets = [
            np.array([0.03, 0.01, 0.01]),
            np.array([0.03, 0.0, 0]),
            np.array([0.03, -0.01, -0.01]),
            np.array([0.02, -0.02, -0.02])
        ]
        
        for offset in finger_offsets:
            finger_pos = grasp_pos + rot_matrix @ offset
            finger_positions.append(finger_pos)
        
        return finger_positions
    
    def _compute_finger_positions_sphere(self, grasp_pos, orientation, radius):
        """Compute finger positions for sphere grasp"""
        rot_matrix = R.from_quat(orientation).as_matrix()
        
        # Distribute fingers around the sphere in a graspable pattern
        finger_positions = []
        
        # Thumb position (opposing other fingers)
        thumb_offset = np.array([0, -0.03, 0])
        thumb_pos = grasp_pos + rot_matrix @ thumb_offset
        finger_positions.append(thumb_pos)
        
        # Other fingers positioned around the sphere
        finger_angles = [0, 2*np.pi/3, 4*np.pi/3]
        for angle in finger_angles:
            x_offset = 0.03 * np.cos(angle)
            y_offset = 0.03 * np.sin(angle)
            offset = np.array([x_offset, y_offset, 0])
            finger_pos = grasp_pos + rot_matrix @ offset
            finger_positions.append(finger_pos)
        
        return finger_positions
    
    def _evaluate_grasp_quality(self, finger_positions: List[np.ndarray], 
                               obj_props: ObjectProperties, 
                               grasp_type: str = 'power') -> float:
        """
        Evaluate the quality of a grasp (simplified model)
        """
        if len(finger_positions) < 2:
            return 0.0
        
        # Calculate grasp quality based on several factors
        quality = 0.0
        
        # 1. Force closure evaluation (simplified)
        # For this example, we'll calculate how well fingers are distributed
        center_of_fingers = np.mean(finger_positions, axis=0)
        
        # Calculate spread of fingers
        spread = sum([np.linalg.norm(p - center_of_fingers) for p in finger_positions])
        quality += min(1.0, spread / 0.1)  # Normalize to 0-1 scale
        
        # 2. Adjust based on grasp type
        if grasp_type == 'precision':
            quality *= 0.8  # Precision grasps generally harder
        elif grasp_type == 'power':
            quality *= 1.0  # Power grasps more reliable
        
        # 3. Consider object properties
        if obj_props.mass > 2.0:  # Heavy objects require better grasps
            quality *= 0.7
        
        # 4. Friction consideration
        if obj_props.friction_coeff < 0.3:  # Low friction surfaces
            quality *= 0.8
        
        # Normalize to 0-1 range
        return min(1.0, max(0.0, quality))
    
    def plan_manipulation_trajectory(self, task: ManipulationTask) -> List[np.ndarray]:
        """
        Plan a manipulation trajectory from grasp to final pose
        """
        # This is a simplified trajectory planning implementation
        # In reality, this would use RRT, RRT*, or other motion planning algorithms
        
        # Assume we have the best grasp position from compute_grasp_candidates
        # For this example, we'll create a simple trajectory
        
        # Example: lift object, move to target, place
        grasp_pos = task.object_properties.com + np.array([0, 0, 0.05])  # Just above object
        lift_pos = grasp_pos.copy()
        lift_pos[2] += 0.2  # Lift 20cm above grasp
        approach_pos = task.target_pose[:3].copy()
        approach_pos[2] += 0.1  # Approach 10cm above target
        place_pos = task.target_pose[:3].copy()
        
        # Create waypoints
        waypoints = [grasp_pos, lift_pos, approach_pos, place_pos]
        
        # Generate trajectory between waypoints
        trajectory = []
        steps_per_segment = 10
        
        for i in range(len(waypoints) - 1):
            start = waypoints[i]
            end = waypoints[i + 1]
            
            for j in range(steps_per_segment):
                t = j / steps_per_segment
                pos = (1 - t) * start + t * end
                trajectory.append(pos)
        
        return trajectory
    
    def inverse_kinematics_arm(self, end_effector_pose: np.ndarray, 
                              arm_configuration: str = 'right') -> np.ndarray:
        """
        Solve inverse kinematics for 7-DOF arm to reach desired end-effector pose
        Simplified analytical solution for 7-DOF arm
        """
        # This is a simplified implementation - in practice, numerical methods
        # or more sophisticated analytical solutions would be used
        target_pos = end_effector_pose[:3]
        target_rot = R.from_quat(end_effector_pose[3:7]) if len(end_effector_pose) >= 7 \
                     else R.from_euler('xyz', [0, 0, 0])
        
        # Simplified 7-DOF arm model: shoulder (3DOF), elbow (1DOF), wrist (3DOF)
        # Link lengths
        l1, l2, l3 = 0.3, 0.3, 0.15  # shoulder-elbow, elbow-wrist, wrist-end effector
        
        # Calculate position for wrist center (wrist joint position)
        # Account for wrist joint to end-effector offset
        wrist_offset = np.array([0.05, 0, 0])  # Typical offset
        rot_matrix = target_rot.as_matrix()
        wrist_center = target_pos - rot_matrix @ wrist_offset
        
        # Calculate shoulder orientation to point toward wrist center
        dx = wrist_center[0]
        dy = wrist_center[1]
        dz = wrist_center[2] - 1.0  # Assuming shoulder at (0,0,1) relative to world
        
        shoulder_azimuth = math.atan2(dy, dx)
        r = math.sqrt(dx**2 + dy**2)
        shoulder_elevation = math.atan2(dz, r)
        
        # Calculate elbow angle using law of cosines
        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        if dist > l1 + l2:
            # Position is out of reach
            shoulder_elbow = 0
            elbow_wrist = 0
        else:
            cos_elbow = (l1**2 + l2**2 - dist**2) / (2 * l1 * l2)
            cos_elbow = np.clip(cos_elbow, -1, 1)
            elbow_angle = math.acos(cos_elbow)
            shoulder_elbow = np.pi - elbow_angle
            
            # Calculate wrist angles to achieve target orientation
            # This is a simplified calculation
            wrist_roll = 0  # Simplified
            wrist_pitch = 0
            wrist_yaw = 0
        
        # Return joint angles [shoulder_azimuth, shoulder_elevation, shoulder_twist, 
        #                      elbow_flexion, wrist_roll, wrist_pitch, wrist_yaw]
        joint_angles = np.array([shoulder_azimuth, shoulder_elevation, 0, 
                                shoulder_elbow, wrist_roll, wrist_pitch, wrist_yaw])
        
        return joint_angles
    
    def compute_grasp_stability(self, grasp: Grasp, obj_props: ObjectProperties) -> float:
        """
        Compute the stability of a grasp under external forces
        """
        # Simplified stability calculation based on grasp wrench space
        # In reality, this would involve more complex force closure analysis
        
        # Calculate grasp stability based on finger positions and object properties
        finger_positions = grasp.finger_positions
        if len(finger_positions) < 2:
            return 0.0
        
        # Calculate center of the grasp
        grasp_center = np.mean(finger_positions, axis=0)
        
        # Calculate the grasp matrix (simplified)
        # The grasp matrix relates joint torques to object wrenches
        # For stability, we need to check if the grasp can resist external wrenches
        
        # For this simplified model, we'll calculate a stability index
        # based on finger distribution and friction
        stability = 0.0
        
        # 1. Distribution measure
        distances = [np.linalg.norm(finger_pos - grasp_center) for finger_pos in finger_positions]
        avg_distance = np.mean(distances)
        stability += min(1.0, avg_distance / 0.05)  # Normalize based on typical grasp size
        
        # 2. Friction contribution
        stability += obj_props.friction_coeff
        
        # 3. Object weight consideration
        stability -= min(0.5, obj_props.mass / 10.0)  # Heavier objects harder to grasp
        
        # Normalize to 0-1 range
        return min(1.0, max(0.0, stability / 2.0))

# Example usage and simulation
def visualize_grasp(grasp: Grasp, obj_props: ObjectProperties):
    """
    Visualize the grasp configuration in 3D
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot object (simplified as a box)
    if obj_props.shape == 'box':
        width, height, depth = obj_props.dimensions
        r = [-width/2, width/2]
        X, Y = np.meshgrid(r, r)
        Z = np.zeros_like(X)
        
        # Plot the 6 faces
        ax.plot_surface(X + obj_props.com[0], Y + obj_props.com[1], Z + obj_props.com[2] - height/2, alpha=0.2, color='blue')
        ax.plot_surface(X + obj_props.com[0], Y + obj_props.com[1], Z + obj_props.com[2] + height/2, alpha=0.2, color='blue')
        
        r = [-width/2, width/2]
        Z, Y = np.meshgrid(r, r)
        X = np.zeros_like(Z)
        ax.plot_surface(X + obj_props.com[0] - depth/2, Y + obj_props.com[1], Z + obj_props.com[2], alpha=0.2, color='blue')
        ax.plot_surface(X + obj_props.com[0] + depth/2, Y + obj_props.com[1], Z + obj_props.com[2], alpha=0.2, color='blue')
        
        X, Z = np.meshgrid(r, r)
        Y = np.zeros_like(X)
        ax.plot_surface(X + obj_props.com[0], Y + obj_props.com[1] - height/2, Z + obj_props.com[2], alpha=0.2, color='blue')
        ax.plot_surface(X + obj_props.com[0], Y + obj_props.com[1] + height/2, Z + obj_props.com[2], alpha=0.2, color='blue')
    
    # Plot finger positions
    for i, pos in enumerate(grasp.finger_positions):
        ax.scatter(pos[0], pos[1], pos[2], color='red', s=100, label=f'Finger {i+1}' if i == 0 else "")
    
    # Plot grasp center
    ax.scatter(grasp.position[0], grasp.position[1], grasp.position[2], 
               color='green', s=200, label='Grasp Center')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'{grasp.grasp_type.title()} Grasp (Quality: {grasp.quality:.2f})')
    ax.legend()
    
    plt.show()

def main():
    print("Humanoid Manipulation and Grasping")
    print("=" * 38)
    
    # Initialize manipulation system
    manipulator = HumanoidManipulation()
    
    # Example 1: Create an object to grasp
    cup_props = ObjectProperties(
        shape='cylinder',
        dimensions=np.array([0.08, 0.1, 0.0]),  # diameter, height, unused
        mass=0.3,
        com=np.array([0.5, 0.2, 0.8]),  # position in world coordinates
        friction_coeff=0.8,
        surface_texture='smooth'
    )
    
    print(f"Object: {cup_props.shape}, mass: {cup_props.mass}kg, position: {cup_props.com}")
    
    # Example 2: Compute grasp candidates
    grasp_candidates = manipulator.compute_grasp_candidates(cup_props)
    
    print(f"Found {len(grasp_candidates)} potential grasps:")
    for i, grasp in enumerate(grasp_candidates[:3]):  # Show top 3
        print(f"  Grasp {i+1}: {grasp.grasp_type}, quality: {grasp.quality:.3f}, "
              f"position: ({grasp.position[0]:.2f}, {grasp.position[1]:.2f}, {grasp.position[2]:.2f})")
    
    if grasp_candidates:
        best_grasp = max(grasp_candidates, key=lambda g: g.quality)
        print(f"\nBest grasp: {best_grasp.grasp_type}, quality: {best_grasp.quality:.3f}")
        
        # Visualize the best grasp
        print("Visualizing the best grasp...")
        # Note: To see the visualization, uncomment the next line when running locally
        # visualize_grasp(best_grasp, cup_props)
    
    # Example 3: Plan a manipulation trajectory
    target_pose = np.array([0.7, 0.0, 1.0])
    task = ManipulationTask(
        object_properties=cup_props,
        target_pose=target_pose,
        constraints=['delicate', 'upright'],
        trajectory=[]
    )
    
    trajectory = manipulator.plan_manipulation_trajectory(task)
    print(f"\nPlanned trajectory with {len(trajectory)} waypoints")
    print(f"Moving from {cup_props.com[:2]} to {target_pose[:2]}")
    
    # Example 4: Calculate inverse kinematics for a position
    end_effector_pose = np.hstack([best_grasp.position, [0, 0, 0, 1]])  # Add orientation placeholder
    try:
        joint_angles = manipulator.inverse_kinematics_arm(end_effector_pose)
        print(f"\nRequired joint angles: {joint_angles[:4]}... radians")  # Show first 4 angles
    except Exception as e:
        print(f"Error in inverse kinematics: {e}")
    
    # Example 5: Calculate grasp stability
    if grasp_candidates:
        stability = manipulator.compute_grasp_stability(best_grasp, cup_props)
        print(f"Grasp stability: {stability:.3f}")
    
    print("\nManipulation planning completed!")

if __name__ == "__main__":
    main()
```

## Simulation

### Manipulation Simulation in Gazebo

Simulating manipulation in Gazebo requires accurate modeling of both the robot and objects:

1. **Grasp Physics**: Modeling friction, contact dynamics, and grasp stability
2. **Collision Detection**: Accurate detection of contacts for grasping
3. **Force/Torque Sensors**: Simulation of fingertip sensors and joint torque
4. **Object Properties**: Accurate mass, friction, and dynamics modeling

### Gazebo Manipulation Configuration

```xml
<!-- Example: Gazebo configuration for manipulation -->
<gazebo reference="gripper_link">
  <disableFixedJointLumping>true</disableFixedJointLumping>
  <self_collide>false</self_collide>
  <enable_gravity>true</enable_gravity>
  <mu1>0.9</mu1>  <!-- Friction coefficient -->
  <mu2>0.9</mu2>  <!-- Secondary friction coefficient -->
  <kp>10000000.0</kp>  <!-- Contact stiffness -->
  <kd>100.0</kd>  <!-- Contact damping -->
  <max_vel>1.0</max_vel>
  <min_depth>0.001</min_depth>
</gazebo>

<!-- Object properties for manipulation -->
<gazebo reference="grasped_object">
  <static>false</static>
  <enable_gravity>true</enable_gravity>
  <mu1>0.6</mu1>
  <mu2>0.6</mu2>
  <material>Gazebo/Blue</material>
  <turnGravityOff>false</turnGravityOff>
</gazebo>
```

### Manipulation Simulation Exercises

1. **Grasp Planning Validation**:
   - Test grasp poses in simulation before real execution
   - Compare planned grasps with successful grasps
   - Analyze failures to improve grasp planners

2. **Dynamic Manipulation**:
   - Simulate moving objects and catching tasks
   - Test manipulation under dynamic conditions
   - Evaluate controller robustness to motion

3. **Multi-Object Manipulation**:
   - Simulate complex tasks with multiple objects
   - Test coordination between both arms
   - Plan multi-step manipulation sequences

4. **Humanoid-Specific Manipulation**:
   - Consider balance constraints during manipulation
   - Test whole-body manipulation planning
   - Evaluate bi-manual coordination tasks

## Exercises

1. **Basic Grasping**:
   - Implement an analytical grasp planner for simple shapes
   - Create a grasp quality evaluation function
   - Design a basic manipulation trajectory

2. **Advanced Grasping**:
   - Implement a data-driven grasp planner using point clouds
   - Create a learning-based grasp selection system
   - Develop adaptive grasping for unknown objects

3. **Simulation Projects**:
   - Create a complete manipulation simulation environment
   - Implement a dual-arm manipulation task
   - Simulate manipulation of deformable objects

4. **Control Implementation**:
   - Implement impedance control for safe manipulation
   - Create force control for delicate objects
   - Develop haptic feedback systems

5. **Real-world Application**:
   - Analyze manipulation strategies of real humanoid robots
   - Compare simulation results with real robot performance
   - Research challenges in transferring manipulation from simulation to reality

## Bibliography & Further Reading

1. Mason, M. (2001). *Mechanics of Robotic Manipulation*. MIT Press.
2. Murray, R. M., Li, Z., & Sastry, S. S. (1994). *A Mathematical Introduction to Robotic Manipulation*. CRC Press.
3. Okamura, A. M., Romano, J. M., & Malec, D. P. (2000). "Metrics for measuring performance in robotic manipulation." *IEEE Conference on Robotics and Automation*.
4. Feix, T., Pawlik, R., Schmiedmayer, H. B., Rodriguez, C. R., & Albarghouti, A. (2015). "Grasp taxonomy of human hand". *IEEE International Conference on Robotics and Automation*.
5. ROS MoveIt Documentation: https://moveit.ros.org/