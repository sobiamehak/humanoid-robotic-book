---
title: Chapter 4 - Dynamics and Control of Humanoid Robots
sidebar_position: 4
---

# Dynamics and Control of Humanoid Robots

## Theory

Robot dynamics is the study of forces and torques that cause motion in robotic systems. For humanoid robots, dynamics is particularly complex due to their multiple interconnected links, underactuation, and the need to maintain balance while performing tasks. Unlike kinematics (which studies motion without forces), dynamics considers the mass, inertia, friction, and external forces that affect robot motion.

### Key Dynamic Concepts for Humanoid Robots

#### Equations of Motion
The motion of a humanoid robot is governed by the Lagrange equations or Newton-Euler equations:

**Lagrange Formulation:**
M(q)q̈ + C(q,q̇)q̇ + g(q) = τ

Where:
- M(q) is the mass matrix
- C(q,q̇) contains Coriolis and centrifugal terms
- g(q) represents gravitational forces
- τ is the vector of joint torques
- q, q̇, q̈ are joint positions, velocities, and accelerations

#### Center of Mass (CoM)
The CoM is critical for humanoid balance:
- Must remain within the support polygon for static stability
- Trajectory planning must consider CoM dynamics during dynamic motions
- Control strategies like DCM (Divergent Component of Motion) use CoM properties

#### Zero Moment Point (ZMP)
ZMP is a critical concept for bipedal locomotion:
- Point where the net moment due to gravity and inertia forces is zero
- Used in walking pattern generation to ensure dynamic stability
- Trajectory should remain within the support polygon

#### Underactuation
Humanoid robots are typically underactuated systems:
- Fewer actuators than degrees of freedom in some configurations
- Requires sophisticated control to maintain balance
- Passive dynamics can be exploited for energy efficiency

### Control Hierarchies in Humanoid Robots

#### High-Level Planning
- Trajectory planning for CoM, feet, and hands
- Gait pattern generation
- Whole-body motion planning

#### Middle-Level Control
- Balance control (e.g., LIPM-based controllers)
- Inverse kinematics for joint positions
- Force distribution among contact points

#### Low-Level Control
- Joint-level PID control
- Motor drivers and amplifiers
- Real-time safety systems

### Walking Pattern Generation

#### Linear Inverted Pendulum Model (LIPM)
- Simplifies the robot to a point mass at CoM
- Used for planning stable walking patterns
- Allows analytical solutions for ZMP trajectories

#### Preview Control
- Uses future reference information to improve tracking
- Reduces tracking errors in dynamic balancing
- Commonly used for ZMP-based walking

### Balance Control Strategies

#### Capture Point Control
- Determines where to step to stop the robot
- Used for push recovery and disturbance rejection
- More general than ZMP for dynamic situations

#### Model Predictive Control (MPC)
- Optimizes control over a prediction horizon
- Handles constraints naturally
- Computationally intensive but effective for balance

## Code

```python
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import solve_continuous_are
import matplotlib.pyplot as plt

class HumanoidDynamics:
    def __init__(self, mass=70.0, height=1.7, com_height=0.9):
        """
        Initialize humanoid dynamics model
        mass: Total robot mass in kg
        height: Robot height in meters
        com_height: Initial center of mass height in meters
        """
        self.mass = mass
        self.height = height
        self.com_height = com_height
        self.g = 9.81  # gravity constant
        
        # Simplified model parameters
        self.inertia = 0.1 * mass * height**2  # Moment of inertia approximation
        
        # Control parameters
        self.kp_com = np.array([100.0, 100.0, 50.0])  # Proportional gains for CoM
        self.kd_com = np.array([20.0, 20.0, 15.0])   # Derivative gains for CoM
        self.kp_ang = np.array([50.0, 50.0, 10.0])   # Proportional gains for angles
        self.kd_ang = np.array([15.0, 15.0, 5.0])    # Derivative gains for angles

    def inverted_pendulum_model(self, t, state, external_force=np.zeros(3)):
        """
        Simplified inverted pendulum model for humanoid dynamics
        state = [x, y, z, vx, vy, vz, phi, theta, psi, phidot, thetadot, psidot]
        where (x,y,z) is CoM position and (phi,theta,psi) are orientation angles
        """
        x, y, z, vx, vy, vz, phi, theta, psi, phidot, thetadot, psidot = state
        
        # Simplified dynamics - point mass with orientation
        # For ZMP calculation: (x, y) = (CoM_x, CoM_y) - (h/g) * (CoM_x_ddot, CoM_y_ddot)
        zmp_x = x - (self.com_height / self.g) * (-self.g * theta)
        zmp_y = y - (self.com_height / self.g) * (self.g * phi)
        
        # Dynamics equations (simplified)
        x_ddot = external_force[0] / self.mass
        y_ddot = external_force[1] / self.mass
        z_ddot = external_force[2] / self.mass - self.g
        
        # Angular acceleration (simplified)
        phi_ddot = -self.g / self.com_height * phi
        theta_ddot = -self.g / self.com_height * theta
        psi_ddot = 0  # No yaw moment in simplified model
        
        return [vx, vy, vz, x_ddot, y_ddot, z_ddot, phidot, thetadot, psidot, 
                phi_ddot, theta_ddot, psi_ddot]

    def linear_inverted_pendulum_model(self, x, y, z, xdot, ydot, zdot):
        """
        Linear Inverted Pendulum Model dynamics for balance control
        Returns ZMP based on current CoM state
        """
        # ZMP = (x, y) - h/g * (ẍ, ÿ) where h is CoM height
        # In LIPM, ẍ = w²(x - x_zmp) and ÿ = w²(y - y_zmp) where w = sqrt(g/h)
        omega = np.sqrt(self.g / self.com_height)
        
        # Calculate expected accelerations for current state
        x_ddot = omega**2 * (x - 0)  # Assuming equilibrium at (0,0)
        y_ddot = omega**2 * (y - 0)
        
        # ZMP calculation
        zmp_x = x - x_ddot / omega**2
        zmp_y = y - y_ddot / omega**2
        
        return zmp_x, zmp_y

    def balance_control_lipm(self, current_state, desired_state):
        """
        Balance control based on Linear Inverted Pendulum Model
        current_state: [x, y, z, xdot, ydot, zdot]
        desired_state: [x_d, y_d, z_d, xdot_d, ydot_d, zdot_d]
        """
        x, y, z, xdot, ydot, zdot = current_state
        x_d, y_d, z_d, xdot_d, ydot_d, zdot_d = desired_state
        
        # Calculate ZMP error
        zmp_current_x, zmp_current_y = self.linear_inverted_pendulum_model(
            x, y, z, xdot, ydot, zdot)
        zmp_desired_x, zmp_desired_y = self.linear_inverted_pendulum_model(
            x_d, y_d, z_d, xdot_d, ydot_d, zdot_d)
        
        # Control law to reduce ZMP error
        omega = np.sqrt(self.g / self.com_height)
        kp = 10.0  # Proportional gain for ZMP control
        
        # Desired acceleration to reduce ZMP error
        x_ddot_desired = omega**2 * (x_d - zmp_current_x + kp * (zmp_desired_x - zmp_current_x))
        y_ddot_desired = omega**2 * (y_d - zmp_current_y + kp * (zmp_desired_y - zmp_current_y))
        
        # Convert to required CoM accelerations
        com_acc = np.array([x_ddot_desired, y_ddot_desired, 0.0])
        
        return com_acc

    def compute_inverse_dynamics(self, q, qdot, qddot, external_forces=None):
        """
        Compute inverse dynamics to find required joint torques
        Using simplified RNEA (Recursive Newton-Euler Algorithm) approach
        """
        # This is a simplified model - for real implementation, use URDF + KDL or Pinocchio
        n_joints = len(q)
        
        # Simplified mass matrix (diagonal for illustration)
        M = np.diag([1.0 + 0.1 * abs(q[i]) for i in range(n_joints)])  # Placeholder
        
        # Coriolis terms (simplified)
        C = np.zeros((n_joints, n_joints))
        for i in range(n_joints):
            C[i, i] = 0.1 * qdot[i]  # Placeholder for Coriolis effects
        
        # Gravity terms (simplified)
        g = np.array([0.5 * np.sin(q[i]) for i in range(n_joints)])  # Placeholder
        
        # Compute required torques: τ = M(q)*q̈ + C(q,q̇)*q̇ + g(q)
        tau = M @ qddot + C @ qdot + g
        
        if external_forces is not None:
            tau += external_forces  # Add effects of external forces
            
        return tau

    def step_controller(self, com_pos, com_vel, foot_position, support_leg='left'):
        """
        Simple step controller for bipedal balance
        """
        # Capture point calculation
        cp_x = com_pos[0] + com_vel[0] / np.sqrt(self.g / self.com_height)
        cp_y = com_pos[1] + com_vel[1] / np.sqrt(self.g / self.com_height)
        
        # Decide if a step is needed (simplified)
        step_needed = abs(cp_x) > 0.1 or abs(cp_y) > 0.1
        
        if step_needed:
            # Calculate where to step to capture the momentum
            step_target_x = com_pos[0] - np.sign(com_vel[0]) * 0.15  # Step width 15cm
            step_target_y = 0.0 if support_leg == 'left' else 0.1     # Base width ~10cm
            
            return True, (step_target_x, step_target_y)
        else:
            return False, None

# Example usage and simulation
def simulate_balance_control():
    """
    Example simulation of balance control for a humanoid robot
    """
    robot = HumanoidDynamics()
    
    # Initial state: [x, y, z, vx, vy, vz, phi, theta, psi, phidot, thetadot, psidot]
    initial_state = [0.0, 0.0, robot.com_height, 0.0, 0.0, 0.0, 
                     0.05, 0.03, 0.0, 0.0, 0.0, 0.0]  # Small initial tilt
    
    # Simulate for 5 seconds
    t_span = (0, 5)
    t_eval = np.linspace(0, 5, 500)
    
    def dynamics_wrapper(t, state):
        return robot.inverted_pendulum_model(t, state)
    
    # Solve the ODE
    solution = solve_ivp(dynamics_wrapper, t_span, initial_state, 
                         t_eval=t_eval, method='RK45')
    
    print(f"Simulation completed with {len(solution.t)} time steps")
    
    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(solution.t, solution.y[0], label='CoM X (m)')
    ax1.plot(solution.t, solution.y[1], label='CoM Y (m)')
    ax1.set_ylabel('Position (m)')
    ax1.set_title('Center of Mass Position Over Time')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(solution.t, solution.y[6], label='Roll (rad)')
    ax2.plot(solution.t, solution.y[7], label='Pitch (rad)')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Orientation (rad)')
    ax2.set_title('Robot Orientation Over Time')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Print final state
    final_state = solution.y[:, -1]
    print(f"Final CoM position: ({final_state[0]:.3f}, {final_state[1]:.3f}, {final_state[2]:.3f}) m")
    print(f"Final orientation: ({final_state[6]:.3f}, {final_state[7]:.3f}, {final_state[8]:.3f}) rad")
    
    return solution

def main():
    print("Humanoid Dynamics and Control")
    print("=" * 40)
    
    # Create robot dynamics model
    robot = HumanoidDynamics()
    
    # Example: Calculate required torques for a motion
    q = np.array([0.1, 0.2, 0.0, -0.1, -0.2, 0.0])  # Joint positions
    qdot = np.array([0.5, 0.3, 0.0, -0.5, -0.3, 0.0])  # Joint velocities
    qddot = np.array([1.0, 0.8, 0.0, -1.0, -0.8, 0.0])  # Joint accelerations
    
    torques = robot.compute_inverse_dynamics(q, qdot, qddot)
    print(f"Required joint torques: {torques[:3]}... N·m")
    
    # Example: Balance control
    current_state = [0.02, 0.01, robot.com_height, 0.05, 0.02, 0.0]  # [x, y, z, xdot, ydot, zdot]
    desired_state = [0.0, 0.0, robot.com_height, 0.0, 0.0, 0.0]
    
    required_acc = robot.balance_control_lipm(current_state, desired_state)
    print(f"Required CoM acceleration: {required_acc} m/s²")
    
    # Example: Step control
    com_pos = [0.05, 0.02]
    com_vel = [0.1, 0.05]
    foot_pos = [0.0, 0.1]  # Right foot position
    
    step_needed, step_target = robot.step_controller(com_pos, com_vel, foot_pos, 'left')
    print(f"Step needed: {step_needed}, Target: {step_target}")
    
    # Uncomment to run simulation
    # simulation_result = simulate_balance_control()

if __name__ == "__main__":
    main()
```

## Simulation

### Dynamics Simulation in Gazebo

Dynamics simulation is crucial for humanoid robots as it helps test control algorithms safely before deployment on real hardware. The simulation must accurately model:

1. **Mass Properties**: Correct mass, center of mass, and inertia tensors for all links
2. **Joint Dynamics**: Friction, motor characteristics, and actuator limits
3. **Contact Physics**: Accurate collision detection and response for balance
4. **External Forces**: Gravity, friction, and external disturbances

### Setting up Dynamics Simulation

```bash
# Install required packages for dynamics simulation
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers
```

### Example URDF with Dynamics Properties

```xml
<!-- Example: humanoid link with dynamics properties -->
<link name="left_thigh">
  <inertial>
    <mass value="5.0" />
    <origin xyz="0 0 -0.2" />
    <inertia ixx="0.1" ixy="0.0" ixz="0.0"
             iyy="0.1" iyz="0.0"
             izz="0.01" />
  </inertial>
  <visual>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.08" length="0.4"/>
    </geometry>
    <material name="light_grey">
      <color rgba="0.7 0.7 0.7 1.0"/>
    </material>
  </visual>
  <collision>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <geometry>
      <capsule radius="0.08" length="0.4"/>
    </geometry>
  </collision>
</link>
```

### Simulation Exercises

1. **Stability Analysis**:
   - Simulate a humanoid standing in single support and observe stability
   - Apply small disturbances and measure recovery time
   - Tune PID parameters for optimal balance

2. **Walking Simulation**:
   - Implement a walking controller using ZMP-based reference trajectories
   - Test walking at different speeds and turning motions
   - Analyze energy efficiency of different gaits

3. **Push Recovery**:
   - Apply external forces to test balance recovery algorithms
   - Evaluate capture point control vs. other methods
   - Test robustness to different disturbance magnitudes

4. **Dynamic Motion**:
   - Simulate complex movements like getting up from a fall
   - Test manipulation tasks with full-body dynamics
   - Evaluate load distribution and balance during dual-arm tasks

## Exercises

1. **Mathematical Foundations**:
   - Derive the equations of motion for a 3-link planar biped using Lagrangian mechanics
   - Derive the ZMP equations from the 3D rigid body dynamics equations
   - Prove the relationship between CoM and ZMP for the Linear Inverted Pendulum Model

2. **Control Implementation**:
   - Implement a ZMP tracking controller for a simulated humanoid
   - Create a balance controller using Model Predictive Control
   - Develop a step timing and location planner for walking

3. **Simulation Projects**:
   - Create a complete URDF model of a humanoid robot with realistic dynamics
   - Implement LIPM-based walking pattern generation
   - Simulate a humanoid performing a simple manipulation task while maintaining balance

4. **Advanced Control**:
   - Implement a whole-body controller that handles multiple tasks simultaneously
   - Create an admittance controller for safe human-robot interaction
   - Develop a learning-based approach for improving balance control

5. **Real-world Application**:
   - Analyze the control strategies used in a state-of-the-art humanoid robot
   - Compare simulation results with real robot performance
   - Research challenges in transferring dynamics controllers from simulation to reality

## Bibliography & Further Reading

1. Featherstone, R. (2008). *Rigid Body Dynamics Algorithms*. Springer.
2. Kajita, S. (2019). *Humanoid Robotics: A Reference*. Springer.
3. Ogata, K. (2010). *Modern Control Engineering*. Prentice Hall.
4. Wight, D., Kubica, E., & Wang, D. (2008). "Introduction to circle criterion safety analysis for control of the one-legged hopper." *Multibody System Dynamics*, 22(4), 393-414.
5. Gazebo Dynamics Documentation: http://gazebosim.org/tutorials?tut=physics