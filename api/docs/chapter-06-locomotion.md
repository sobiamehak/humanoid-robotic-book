---
title: Chapter 6 - Locomotion and Gait Planning
sidebar_position: 6
---

# Locomotion and Gait Planning

## Theory

Locomotion is one of the most critical capabilities for humanoid robots, enabling them to navigate diverse human environments. Unlike wheeled or tracked robots, humanoid robots must manage complex multi-link dynamics while maintaining balance and adapting to variable terrain. This chapter covers the principles, methods, and algorithms for generating stable and efficient walking patterns.

### Fundamentals of Humanoid Locomotion

#### Balance vs. Stability
- **Static Stability**: Center of mass remains within support polygon at all times
- **Dynamic Stability**: Robot remains balanced during motion with active control
- **Stability Margins**: How much disturbance the robot can handle before falling

#### Gait Parameters
- **Step Length**: Distance between consecutive foot placements
- **Step Width**: Lateral distance between feet (stride width)
- **Step Height**: Vertical clearance of swinging foot
- **Double Support Time**: Time when both feet are on the ground
- **Single Support Time**: Time when only one foot is on the ground
- **Walking Speed**: Rate of forward progression

### Key Locomotion Patterns

#### Walking (Bipedal)
- Alternating support between legs
- Periodic motion with single and double support phases
- Requires sophisticated balance control

#### Running
- Both feet leave the ground during the gait cycle
- Higher speeds with greater control complexity
- Less stable but more efficient for faster locomotion

#### Standing
- Single support with CoM over support polygon
- Requires balance control to maintain posture
- Can be single or double support depending on stance

#### Climbing and Stairs
- Requires precise foot placement and coordination
- Often uses hand support in addition to feet
- Planning considers both kinematic and dynamic constraints

### Gait Planning Approaches

#### Model-Based Approaches
- **Linear Inverted Pendulum Model (LIPM)**: Simplifies robot to point mass
- **Cart-Table Model**: Extends LIPM with variable height
- **Single Rigid Body Model (SRBM)**: Considers full robot mass distribution

#### Pattern Generation Methods
- **Preview Control**: Uses future trajectory information
- **MPC (Model Predictive Control)**: Optimizes over prediction horizon
- **Virtual Model Control**: Treats robot as virtual spring-damper system

#### Learning-Based Approaches
- **Reinforcement Learning**: Learns optimal control policies
- **Imitation Learning**: Mimics human or expert demonstrations
- **Central Pattern Generators**: Neural network models of biological rhythms

### Balance Control for Locomotion

#### Zero Moment Point (ZMP)
- Critical for stable walking: net moment is zero at contact points
- Trajectory should remain within support polygon
- Used in many walking pattern generators

#### Capture Point
- Location where robot should step to come to a stop
- More general than ZMP for dynamic situations
- Used in push recovery and disturbance handling

#### Divergent Component of Motion (DCM)
- Extension of Capture Point concept
- Useful for dynamic balance control
- Provides global stability measure

### Terrain Adaptation

#### Flat Ground Walking
- Most common scenario for initial development
- Focus on balance and basic gait patterns
- Good starting point for control algorithm testing

#### Uneven Terrain
- Requires online adaptation of step locations
- May need different gaits (e.g., crawling, climbing)
- Advanced perception for terrain classification

#### Stairs and Steps
- Requires precise foot placement control
- Often uses hand support for stability
- Different kinematic and dynamic considerations

## Code

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, interpolate
from scipy.optimize import minimize
import math

class HumanoidGaitPlanner:
    def __init__(self, robot_height=0.9, step_length=0.3, step_width=0.2, 
                 com_height=0.85, sampling_time=0.01):
        """
        Initialize gait planner for humanoid robot
        """
        self.robot_height = robot_height
        self.step_length = step_length
        self.step_width = step_width
        self.com_height = com_height  # Center of mass height
        self.sampling_time = sampling_time
        self.g = 9.81  # gravity constant
        
        # Walking parameters
        self.omega = np.sqrt(self.g / self.com_height)  # LIPM frequency
        self.single_support_time = 0.7  # Time for single support phase (sec)
        self.double_support_time = 0.1  # Time for double support phase (sec)
        self.walking_speed = 0.3  # Target walking speed (m/s)
        
        # Foot placement parameters
        self.foot_size = [0.15, 0.08]  # Length and width of foot
        
    def generate_zmp_trajectory(self, start_pos, goal_pos, step_count):
        """
        Generate ZMP trajectory for walking between start and goal positions
        """
        # Calculate required steps
        distance = np.linalg.norm(np.array(goal_pos) - np.array(start_pos))
        required_steps = max(2, int(distance / self.step_length) + 1)
        
        # Generate footsteps
        footsteps = self.generate_footsteps(start_pos, goal_pos, required_steps)
        
        # Generate ZMP trajectory based on footsteps
        zmp_x, zmp_y, time_vec = self.plan_zmp_trajectory(footsteps)
        
        return zmp_x, zmp_y, time_vec, footsteps
    
    def generate_footsteps(self, start_pos, goal_pos, step_count):
        """
        Generate footsteps for walking trajectory
        """
        footsteps = []
        
        # Start with current position
        # Assuming starting stance: left foot at start_pos, right foot offset by step_width
        left_foot = [start_pos[0], start_pos[1] + self.step_width/2, start_pos[2]]
        right_foot = [start_pos[0], start_pos[1] - self.step_width/2, start_pos[2]]
        
        # Determine walking direction
        direction = np.array(goal_pos) - np.array(start_pos)
        direction = direction / np.linalg.norm(direction)
        
        # Generate alternating steps
        support_foot = 'right'  # Start with right foot support, move left foot first
        
        for i in range(step_count):
            if support_foot == 'right':
                # Move left foot forward
                new_left_x = left_foot[0] + self.step_length * direction[0]
                new_left_y = left_foot[1] + self.step_width * direction[1] * (-1)**i
                footsteps.append(('left', [new_left_x, new_left_y, start_pos[2]]))
                left_foot = [new_left_x, new_left_y, start_pos[2]]
                support_foot = 'left'
            else:
                # Move right foot forward
                new_right_x = right_foot[0] + self.step_length * direction[0]
                new_right_y = right_foot[1] + self.step_width * direction[1] * (-1)**i
                footsteps.append(('right', [new_right_x, new_right_y, start_pos[2]]))
                right_foot = [new_right_x, new_right_y, start_pos[2]]
                support_foot = 'right'
        
        return footsteps
    
    def plan_zmp_trajectory(self, footsteps):
        """
        Plan ZMP trajectory based on foot placement
        """
        # Calculate total walking duration
        gait_cycle_time = self.single_support_time + self.double_support_time
        total_time = len(footsteps) * gait_cycle_time
        
        # Generate time vector
        time_vec = np.arange(0, total_time, self.sampling_time)
        
        # Initialize ZMP trajectory
        zmp_x = np.zeros(len(time_vec))
        zmp_y = np.zeros(len(time_vec))
        
        # Fill ZMP based on support foot and expected dynamics
        for i, t in enumerate(time_vec):
            cycle_index = int(t / gait_cycle_time)
            time_in_cycle = t % gait_cycle_time
            
            if cycle_index < len(footsteps):
                # Determine which foot is in support
                if time_in_cycle < self.double_support_time:
                    # Double support phase - ZMP transitions between feet
                    phase_ratio = time_in_cycle / self.double_support_time
                    if cycle_index == 0:
                        # At start, ZMP is centered between initial feet
                        zmp_x[i] = 0
                        zmp_y[i] = 0
                    else:
                        # Transition from previous support foot to current
                        prev_foot = footsteps[cycle_index-1][1] if cycle_index > 0 else [0, 0, 0]
                        curr_foot = footsteps[cycle_index][1]
                        
                        zmp_x[i] = prev_foot[0] * (1 - phase_ratio) + curr_foot[0] * phase_ratio
                        zmp_y[i] = prev_foot[1] * (1 - phase_ratio) + curr_foot[1] * phase_ratio
                else:
                    # Single support phase - ZMP near supporting foot
                    support_foot = footsteps[cycle_index][1]
                    
                    # Add small offset for dynamic stability
                    offset_x = 0.02 * np.sin(2 * np.pi * (time_in_cycle - self.double_support_time) / 
                                            (self.single_support_time))
                    offset_y = 0.01 * np.cos(2 * np.pi * (time_in_cycle - self.double_support_time) / 
                                            (self.single_support_time))
                    
                    zmp_x[i] = support_foot[0] + offset_x
                    zmp_y[i] = support_foot[1] + offset_y
        
        return zmp_x, zmp_y, time_vec
    
    def solve_inverse_kinematics(self, target_foot_pos, leg_type='left'):
        """
        Solve inverse kinematics for 3-DOF leg (simplified)
        target_foot_pos: [x, y, z] in base frame
        """
        # Simplified 3-DOF leg (hip abduction, hip flexion, knee flexion)
        # This is a planar approximation
        
        # Leg dimensions (simplified)
        thigh_length = 0.4  # 40cm
        shin_length = 0.4  # 40cm
        
        x, y, z = target_foot_pos
        
        # Calculate hip abduction (for lateral movement)
        hip_abd = math.atan2(y, -z)
        
        # Project to sagittal plane
        dist_from_hip = math.sqrt(x**2 + (z)**2)
        
        if dist_from_hip > thigh_length + shin_length:
            raise ValueError("Position out of reach")
        
        # Calculate knee angle using law of cosines
        cos_knee = (thigh_length**2 + shin_length**2 - dist_from_hip**2) / (2 * thigh_length * shin_length)
        cos_knee = np.clip(cos_knee, -1, 1)  # Clamp for numerical errors
        knee_angle = math.pi - math.acos(cos_knee)
        
        # Calculate hip angles
        a1 = thigh_length
        a2 = shin_length
        k1 = a1 + a2 * math.cos(knee_angle)
        k2 = a2 * math.sin(knee_angle)
        
        alpha = math.atan2(z, x)
        beta = math.atan2(k2, k1)
        
        hip_flexion = alpha + (math.pi/2 - beta)
        
        return np.array([hip_abd, hip_flexion, -knee_angle])
    
    def generate_com_trajectory(self, zmp_trajectory, time_vec):
        """
        Generate CoM trajectory from ZMP trajectory using LIPM
        """
        # Use the relationship: ZMP = CoM - (h/g) * CoM_ddot
        # Rearranging: CoM_ddot = (g/h) * (CoM - ZMP)
        # This creates a differential equation that we can solve
        
        com_x = np.zeros_like(zmp_trajectory[0])
        com_y = np.zeros_like(zmp_trajectory[1])
        com_z = np.full_like(zmp_trajectory[0], self.com_height)
        
        # Initial conditions
        if len(zmp_trajectory[0]) > 0:
            com_x[0] = zmp_trajectory[0][0]  # Start near ZMP
            com_y[0] = zmp_trajectory[1][0]
        
        # Use numerical integration to solve the differential equation
        for i in range(1, len(time_vec)):
            dt = self.sampling_time
            
            # Compute CoM acceleration based on ZMP deviation
            com_acc_x = self.omega**2 * (com_x[i-1] - zmp_trajectory[0][i-1])
            com_acc_y = self.omega**2 * (com_y[i-1] - zmp_trajectory[1][i-1])
            
            # Integrate to get velocity and position
            com_x[i] = com_x[i-1] + dt * self.walking_speed + dt**2 * com_acc_x / 2
            com_y[i] = com_y[i-1] + dt * com_acc_y / 2  # Initially assume small velocity
            
        return com_x, com_y, com_z
    
    def generate_joint_trajectories(self, com_trajectory, footsteps, time_vec):
        """
        Generate joint trajectories from CoM and foot positions
        """
        # Simplified approach: generate joint positions for each part of gait
        num_joints = 6  # 3 joints for each leg (hip_abd, hip_flex, knee)
        joint_positions = np.zeros((len(time_vec), num_joints))
        
        # Calculate gait phase
        gait_cycle_time = self.single_support_time + self.double_support_time
        current_support_foot = 'left'
        
        for i, t in enumerate(time_vec):
            cycle_index = int(t / gait_cycle_time)
            
            # Determine support foot based on gait phase
            time_in_cycle = t % gait_cycle_time
            if time_in_cycle > self.double_support_time:
                # Single support - determine from cycle
                current_support_foot = 'right' if cycle_index % 2 == 0 else 'left'
            else:
                # Double support - interpolate
                current_support_foot = 'double'
            
            # Calculate joint positions based on desired CoM and foot positions
            com_pos = [com_trajectory[0][i], com_trajectory[1][i], com_trajectory[2][i]]
            
            # Simplified: set some basic joint positions
            # In reality, this would use full inverse kinematics
            joint_positions[i, :] = self.calculate_leg_joints(com_pos, current_support_foot, i, time_vec)
        
        return joint_positions
    
    def calculate_leg_joints(self, com_pos, support_foot, time_index, time_vec):
        """
        Calculate leg joint positions for balance
        """
        # This is a simplified placeholder
        # In reality, this would implement complex inverse kinematics
        # based on CoM position, support foot, and gait phase
        
        # For demonstration, return basic positions with small variations
        joints = np.zeros(6)
        
        # Basic standing position
        joints[0] = 0.0   # Left hip abduction
        joints[1] = 0.0   # Left hip flexion
        joints[2] = 0.0   # Left knee flexion
        joints[3] = 0.0   # Right hip abduction
        joints[4] = 0.0   # Right hip flexion
        joints[5] = 0.0   # Right knee flexion
        
        # Add small variations based on time for walking motion
        phase = (time_index / len(time_vec)) * 2 * np.pi
        joints[1] += 0.1 * np.sin(phase)  # Hip flexion oscillation
        joints[4] += 0.1 * np.sin(phase)  # Hip flexion oscillation
        joints[2] += 0.2 * np.cos(phase)  # Knee flexion oscillation
        joints[5] += 0.2 * np.cos(phase)  # Knee flexion oscillation
        
        return joints

    def plan_walking_trajectory(self, start_pos, goal_pos, step_count):
        """
        Complete walking trajectory planner
        """
        # Generate ZMP trajectory
        zmp_x, zmp_y, time_vec, footsteps = self.generate_zmp_trajectory(start_pos, goal_pos, step_count)
        
        # Generate CoM trajectory
        com_x, com_y, com_z = self.generate_com_trajectory((zmp_x, zmp_y), time_vec)
        
        # Generate joint trajectories
        joint_positions = self.generate_joint_trajectories((com_x, com_y, com_z), footsteps, time_vec)
        
        # Prepare complete trajectory
        trajectory = {
            'time': time_vec,
            'zmp': (zmp_x, zmp_y),
            'com': (com_x, com_y, com_z),
            'footsteps': footsteps,
            'joints': joint_positions
        }
        
        return trajectory

# Example usage and simulation
def simulate_walking():
    """
    Example simulation of humanoid walking
    """
    # Initialize gait planner
    planner = HumanoidGaitPlanner()
    
    # Define start and goal positions
    start_pos = [0.0, 0.0, 0.0]
    goal_pos = [2.0, 0.5, 0.0]  # Walk 2m forward, 0.5m to the side
    step_count = 8
    
    # Plan the walking trajectory
    trajectory = planner.plan_walking_trajectory(start_pos, goal_pos, step_count)
    
    print(f"Planned walking trajectory with {step_count} steps")
    print(f"Trajectory duration: {trajectory['time'][-1]:.2f} seconds")
    print(f"Footsteps: {len(trajectory['footsteps'])}")
    
    # Print first few footsteps
    for i, (foot, pos) in enumerate(trajectory['footsteps'][:5]):
        print(f"  Step {i+1}: {foot} foot at ({pos[0]:.2f}, {pos[1]:.2f})")
    
    # Plot results
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot footstep plan in X-Y plane
    left_x, left_y = [], []
    right_x, right_y = [], []
    
    for foot, pos in trajectory['footsteps']:
        if foot == 'left':
            left_x.append(pos[0])
            left_y.append(pos[1])
        else:
            right_x.append(pos[0])
            right_y.append(pos[1])
    
    axes[0, 0].plot(left_x, left_y, 'b-o', label='Left Foot', markersize=8)
    axes[0, 0].plot(right_x, right_y, 'r-s', label='Right Foot', markersize=8)
    axes[0, 0].set_xlabel('X (m)')
    axes[0, 0].set_ylabel('Y (m)')
    axes[0, 0].set_title('Footstep Plan')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Plot ZMP trajectory
    axes[0, 1].plot(trajectory['time'], trajectory['zmp'][0], 'g-', label='ZMP X')
    axes[0, 1].plot(trajectory['time'], trajectory['zmp'][1], 'm-', label='ZMP Y')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Position (m)')
    axes[0, 1].set_title('ZMP Trajectory')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Plot CoM trajectory
    axes[1, 0].plot(trajectory['com'][0], trajectory['com'][1], 'k-', linewidth=2, label='CoM Path')
    axes[1, 0].set_xlabel('X (m)')
    axes[1, 0].set_ylabel('Y (m)')
    axes[1, 0].set_title('Center of Mass Trajectory')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Plot joint positions over time (first few joints)
    time_subset = trajectory['time'][:500]  # First 500 points for clarity
    joints_subset = trajectory['joints'][:500, :4]  # First 4 joints
    
    axes[1, 1].plot(time_subset, joints_subset[:, 0], label='Left Hip ABD')
    axes[1, 1].plot(time_subset, joints_subset[:, 1], label='Left Hip FLEX')
    axes[1, 1].plot(time_subset, joints_subset[:, 2], label='Left Knee FLEX')
    axes[1, 1].plot(time_subset, joints_subset[:, 3], label='Right Hip ABD')
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('Joint Angle (rad)')
    axes[1, 1].set_title('Joint Angles Over Time')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.show()

def main():
    print("Humanoid Locomotion and Gait Planning")
    print("=" * 45)
    
    # Initialize gait planner
    planner = HumanoidGaitPlanner()
    
    # Example: simple gait planning
    start_pos = [0.0, 0.0, 0.0]
    goal_pos = [1.0, 0.0, 0.0]
    
    # Plan walking trajectory
    trajectory = planner.plan_walking_trajectory(start_pos, goal_pos, step_count=4)
    
    print(f"Walked from {start_pos} to approximately {goal_pos}")
    print(f"Number of steps: {len(trajectory['footsteps'])}")
    print(f"Trajectory duration: {trajectory['time'][-1]:.2f} seconds")
    
    # Calculate some metrics
    total_distance = np.sqrt((goal_pos[0] - start_pos[0])**2 + (goal_pos[1] - start_pos[1])**2)
    avg_speed = total_distance / trajectory['time'][-1]
    print(f"Average walking speed: {avg_speed:.2f} m/s")
    
    # Example inverse kinematics
    try:
        target_foot_pos = [0.3, 0.1, -0.8]  # Forward, lateral, vertical
        joint_angles = planner.solve_inverse_kinematics(target_foot_pos)
        print(f"Required joint angles for foot position {target_foot_pos}:")
        print(f"  [Hip ABD, Hip FLEX, Knee FLEX]: {joint_angles}")
    except ValueError as e:
        print(f"Error in inverse kinematics: {e}")
    
    # Uncomment to run full simulation with plots
    # simulate_walking()
    
    print("\nGait planning completed!")

if __name__ == "__main__":
    main()
```

## Simulation

### Walking Simulation in Gazebo

Simulating walking in Gazebo requires careful attention to physics parameters and control implementations:

1. **Physics Engine Settings**: Proper configuration of ODE or Bullet for realistic contact dynamics
2. **Control Integration**: Realistic control delays and actuator dynamics
3. **Terrain Models**: Accurate representation of surfaces with appropriate friction
4. **Sensor Simulation**: Realistic sensor models for feedback control

### Example Gazebo Physics Configuration

```xml
<!-- physics parameters for humanoid simulation -->
<physics type="ode">
  <max_step_size>0.001</max_step_size>  <!-- Smaller steps for stability -->
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>  <!-- High update rate for control -->
  <gravity>0 0 -9.8</gravity>
  <ode>
    <solver>
      <type>quick</type>
      <iters>100</iters>  <!-- More iterations for contact stability -->
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0</cfm>
      <erp>0.2</erp>  <!-- Error reduction parameter for contacts -->
      <contact_max_correcting_vel>1.0</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

### Walking Pattern Generation Exercises

1. **ZMP-Based Walking**:
   - Implement a ZMP-based walking pattern generator
   - Test with different step lengths and widths
   - Evaluate stability margins during walking

2. **MPC Walking Control**:
   - Implement Model Predictive Control for walking
   - Test robustness to disturbances and uneven terrain
   - Compare with traditional control approaches

3. **Adaptive Gait**:
   - Implement gait adaptation for different walking speeds
   - Create controllers that adjust to terrain changes
   - Test recovery from external disturbances

4. **Multi-terrain Walking**:
   - Modify walking patterns for stairs, slopes, and rough terrain
   - Implement terrain classification and gait selection
   - Validate in simulation with various surface types

## Exercises

1. **Basic Walking Patterns**:
   - Implement a simple ZMP-based walking pattern generator
   - Create a 2D walking simulation for a simplified biped
   - Test stability of different walking parameters

2. **Control Implementation**:
   - Implement a balance controller using PID control
   - Create a walking controller using preview control
   - Develop a push recovery system for balance

3. **Simulation Projects**:
   - Create a complete walking simulation in Gazebo
   - Implement a 3D walking pattern generator
   - Simulate walking on different terrain types

4. **Advanced Locomotion**:
   - Implement dynamic walking using DCM-based control
   - Create a climbing or stair navigation system
   - Develop learning-based control for walking

5. **Real-world Application**:
   - Analyze the walking strategies of state-of-the-art humanoid robots
   - Compare simulation performance with real robot results
   - Research challenges in transferring walking controllers from simulation to reality

## Bibliography & Further Reading

1. Kajita, S., et al. (2006). *Biped Walking Pattern Generation by Using Preview Control of Zero-Moment Point*. IEEE/RSJ International Conference on Intelligent Robots and Systems.
2. Pratt, J., & Hurst, J. (2008). "Virtual model control: A framework for control of legged robots." *American Control Conference*.
3. Hof, H. (2008). "The 'extrapolated center of mass' concept suggests a simple control of balance in walking." *Human Movement Science*, 27(1), 117-128.
4. Wensing, P., & Orin, D. (2013). "Improved computation of the jacobian matrix for a biped robot using velocity propagation." *IEEE Transactions on Robotics*, 29(6), 1511-1518.
5. ROS Control Documentation: http://wiki.ros.org/ros_control