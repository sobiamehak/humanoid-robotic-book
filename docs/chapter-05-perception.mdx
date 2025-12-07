---
title: Chapter 5 - Perception Systems in Humanoid Robots
sidebar_position: 5
---

# Perception Systems in Humanoid Robots

## Theory

Perception is the foundation of Physical AI - the ability for robots to sense, interpret, and understand their environment. For humanoid robots, perception systems must process multimodal data from various sensors to enable safe navigation, object manipulation, and effective interaction with human environments.

### Core Perception Capabilities

1. **Visual Perception**: Processing of images and video to identify objects, people, and environments
2. **Spatial Perception**: Understanding 3D structure and layout of the environment
3. **Auditory Perception**: Processing sound and speech for communication and environmental awareness
4. **Tactile Perception**: Sensing contact, force, and texture through touch
5. **Proprioception**: Understanding the robot's own pose, joint angles, and balance state

### Key Challenges in Humanoid Perception

1. **Multimodal Integration**: Combining information from different sensor types into a coherent understanding
2. **Real-time Processing**: Processing large amounts of sensor data within strict timing constraints
3. **Robustness**: Operating reliably in varied, dynamic environments
4. **Scalability**: Handling unknown objects, scenarios, and environments
5. **Human-Centric Design**: Recognizing and understanding human behavior, intentions, and social cues

### Essential Sensors for Humanoid Robots

#### Cameras
- **RGB Cameras**: Capture color images for object recognition and scene understanding
- **Stereo Cameras**: Provide depth information for 3D reconstruction
- **RGB-D Cameras**: Combine color and depth sensing in a single device (e.g., Intel RealSense, Kinect)
- **Fish-eye Cameras**: Provide wide field of view for environmental awareness

#### LiDAR (Light Detection and Ranging)
- **3D LiDAR**: Create accurate 3D point clouds of the environment
- **2D LiDAR**: Provide planar depth information for navigation and obstacle detection
- **Solid-state LiDAR**: Emerging technology offering lower cost and higher reliability

#### Inertial Sensors
- **IMU (Inertial Measurement Unit)**: Measure acceleration, angular velocity, and orientation
- **Gyroscopes**: Precise measurement of angular velocity
- **Accelerometers**: Measure linear acceleration and infer orientation relative to gravity

#### Force/Torque Sensors
- **Six-axis Force/Torque Sensors**: Measure forces and moments at joints (especially wrists and feet)
- **Tactile Sensors**: Distributed pressure sensing on hands and feet
- **Joint Torque Sensors**: Measure forces experienced by joint actuators

### Perception Pipeline Architecture

A typical humanoid perception system follows this pipeline:

1. **Sensor Acquisition**: Raw data collection from all sensors
2. **Preprocessing**: Noise filtering, calibration, and data conditioning
3. **Feature Extraction**: Identifying relevant patterns and structures in sensor data
4. **Object Recognition**: Identifying and classifying objects in the environment
5. **Scene Understanding**: Contextual interpretation of the environment
6. **State Estimation**: Tracking the robot's position, orientation, and balance state
7. **Fusion**: Combining information from multiple sensors and modalities
8. **Output Generation**: Structured representations for planning and control

### Spatial Perception

Spatial perception is critical for humanoid robots operating in 3D human environments:

- **SLAM (Simultaneous Localization and Mapping)**: Building maps while determining robot position
- **3D Reconstruction**: Creating geometric models of objects and environments
- **Occupancy Grids**: Probabilistic representations of free vs. occupied space
- **Topological Maps**: Higher-level representations of navigable paths and locations

### Social Perception

Humanoid robots must also perceive and understand human social cues:

- **Face Detection and Recognition**: Identifying and recognizing human faces
- **Gesture Recognition**: Understanding human hand and body gestures
- **Emotion Recognition**: Inferring human emotional states from facial expressions and voice
- **Intention Recognition**: Predicting human intentions from observed behavior

## Code

```python
import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R
import open3d as o3d
from dataclasses import dataclass
from typing import List, Tuple, Optional
import rospy
from sensor_msgs.msg import Image, PointCloud2, CameraInfo
from geometry_msgs.msg import Point, Pose
from cv_bridge import CvBridge
import message_filters

@dataclass
class ObjectDetection:
    """Represents a detected object"""
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x, y, width, height
    center_3d: Optional[np.ndarray] = None  # 3D position in world coordinates
    dimensions: Optional[np.ndarray] = None  # width, height, depth

@dataclass
class HumanoidPerceptionOutput:
    """Complete perception output for humanoid robot"""
    objects: List[ObjectDetection]
    robot_pose: Pose  # Current robot position and orientation
    camera_pose: Pose  # Camera position and orientation relative to robot
    point_cloud: Optional[np.ndarray] = None  # 3D point cloud data
    floor_normal: Optional[np.ndarray] = None  # Normal vector of ground plane
    support_polygon: Optional[np.ndarray] = None  # Convex hull of support feet

class HumanoidPerception:
    def __init__(self):
        self.cv_bridge = CvBridge()
        
        # Camera intrinsic parameters (example values - should be calibrated)
        self.fx = 525.0  # Focal length x
        self.fy = 525.0  # Focal length y
        self.cx = 319.5  # Principal point x
        self.cy = 239.5  # Principal point y
        
        # Initialize Open3D visualizer if needed
        self.vis = None
        
        # Object detection model (placeholder - would use YOLO, Detectron2, etc. in practice)
        # For this example, we'll use a simple color-based detection as a placeholder
        self.object_classes = {
            'cup': ([0, 100, 200], [20, 140, 255]),  # Upper and lower HSV bounds for cup color
            'book': ([100, 50, 50], [130, 255, 255]), # Blue book
            'person': ([0, 0, 100], [20, 50, 200])   # Skin tone range
        }

    def process_camera_image(self, image_msg: Image) -> np.ndarray:
        """Convert ROS Image message to OpenCV image"""
        cv_image = self.cv_bridge.imgmsg_to_cv2(image_msg, "bgr8")
        return cv_image

    def detect_objects(self, image: np.ndarray) -> List[ObjectDetection]:
        """Detect objects in the image using color-based detection (placeholder)"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        detections = []
        
        for class_name, (lower, upper) in self.object_classes.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Filter by area to avoid small noise
                if cv2.contourArea(contour) > 500:
                    # Get bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate center of bounding box
                    center_x, center_y = x + w//2, y + h//2
                    
                    # For this example, confidence is based on contour area
                    confidence = min(0.95, cv2.contourArea(contour) / (image.shape[0] * image.shape[1]))
                    
                    detection = ObjectDetection(
                        class_name=class_name,
                        confidence=confidence,
                        bbox=(x, y, w, h)
                    )
                    detections.append(detection)
        
        # Sort detections by confidence
        detections.sort(key=lambda x: x.confidence, reverse=True)
        return detections[:5]  # Return top 5 detections

    def depth_to_3d(self, depth_image: np.ndarray, detections: List[ObjectDetection]) -> List[ObjectDetection]:
        """Estimate 3D positions of detected objects using depth data"""
        for detection in detections:
            x, y, w, h = detection.bbox
            
            # Get center pixel of bounding box
            center_x, center_y = x + w//2, y + h//2
            
            # Get depth at that pixel
            depth_val = depth_image[center_y, center_x]
            
            # Convert pixel coordinates to 3D world coordinates
            if depth_val > 0:  # Valid depth
                z_world = depth_val
                x_world = (center_x - self.cx) * z_world / self.fx
                y_world = (center_y - self.cy) * z_world / self.fy
                
                detection.center_3d = np.array([x_world, y_world, z_world])
        
        return detections

    def estimate_floor_plane(self, point_cloud: np.ndarray, threshold=0.01) -> Tuple[np.ndarray, float]:
        """Estimate ground plane using RANSAC"""
        # Convert to Open3D point cloud format
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_cloud)
        
        # Estimate plane using RANSAC
        plane_model, inliers = pcd.segment_plane(
            distance_threshold=threshold,
            ransac_n=3,
            num_iterations=1000
        )
        
        # Extract plane parameters: ax + by + cz + d = 0
        [a, b, c, d] = plane_model
        
        # Normal vector of the plane
        normal = np.array([a, b, c])
        normal = normal / np.linalg.norm(normal)
        
        # Distance from origin to plane
        distance = abs(d) / np.linalg.norm(normal)
        
        return normal, distance

    def extract_support_polygon(self, robot_pose: Pose, foot_positions: List[np.ndarray]) -> np.ndarray:
        """Calculate support polygon from contact points (e.g., feet)"""
        # In a real implementation, this would use force/torque sensor data
        # to determine which feet are in contact with the ground
        
        # For this example, assume both feet are in contact
        # Convert foot positions to 2D for convex hull calculation
        foot_points_2d = np.array([[pos[0], pos[1]] for pos in foot_positions])
        
        # Calculate convex hull (simplified - would use scipy's ConvexHull in practice)
        # This is a placeholder for the actual convex hull calculation
        support_polygon = foot_points_2d  # Simplified
        
        return support_polygon

    def process_point_cloud(self, points: np.ndarray) -> np.ndarray:
        """Process raw point cloud data to remove noise and downsample"""
        # Statistical outlier removal
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        
        # Remove statistical outliers
        cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        filtered_points = np.asarray(cl.points)
        
        # Downsample if too dense
        if len(filtered_points) > 10000:
            indices = np.random.choice(len(filtered_points), 
                                     size=10000, replace=False)
            filtered_points = filtered_points[indices]
        
        return filtered_points

    def integrate_sensor_data(self, 
                            image: np.ndarray, 
                            depth: np.ndarray, 
                            imu_data: dict) -> HumanoidPerceptionOutput:
        """Integrate data from multiple sensors to create perception output"""
        # 1. Detect objects in the image
        detections = self.detect_objects(image)
        
        # 2. Estimate 3D positions from depth
        detections = self.depth_to_3d(depth, detections)
        
        # 3. Estimate robot pose from IMU data
        robot_pose = self.estimate_robot_pose_from_imu(imu_data)
        
        # 4. Process point cloud data
        point_cloud = self.create_point_cloud(depth)
        filtered_cloud = self.process_point_cloud(point_cloud)
        
        # 5. Estimate floor plane
        floor_normal, floor_distance = self.estimate_floor_plane(filtered_cloud)
        
        # 6. Extract support polygon (simplified with assumed foot positions)
        foot_positions = [np.array([0.1, -0.1, 0.0]), np.array([0.1, 0.1, 0.0])]
        support_polygon = self.extract_support_polygon(robot_pose, foot_positions)
        
        # Create output structure
        output = HumanoidPerceptionOutput(
            objects=detections,
            robot_pose=robot_pose,
            camera_pose=self.estimate_camera_pose(robot_pose),
            point_cloud=filtered_cloud,
            floor_normal=floor_normal,
            support_polygon=support_polygon
        )
        
        return output

    def estimate_robot_pose_from_imu(self, imu_data: dict) -> Pose:
        """Estimate robot pose from IMU data (simplified)"""
        # This is a simplified example - real implementation would use
        # sensor fusion with other data sources
        pose = Pose()
        
        # Extract orientation from IMU quaternion
        pose.orientation.x = imu_data.get('orientation_x', 0.0)
        pose.orientation.y = imu_data.get('orientation_y', 0.0)
        pose.orientation.z = imu_data.get('orientation_z', 0.0)
        pose.orientation.w = imu_data.get('orientation_w', 1.0)
        
        # Position would come from other sensors (e.g., encoders, SLAM)
        # For this example, assume relative position
        pose.position.x = imu_data.get('position_x', 0.0)
        pose.position.y = imu_data.get('position_y', 0.0)
        pose.position.z = imu_data.get('position_z', 0.8)  # Typical humanoid height
        
        return pose

    def estimate_camera_pose(self, robot_pose: Pose) -> Pose:
        """Estimate camera pose relative to robot base"""
        # Simplified: camera is fixed relative to robot
        camera_pose = Pose()
        
        # Assuming camera is mounted on the head, looking forward
        camera_pose.position.x = robot_pose.position.x
        camera_pose.position.y = robot_pose.position.y
        camera_pose.position.z = robot_pose.position.z + 0.1  # 10cm above robot origin
        
        # Camera orientation: aligned with robot head
        camera_pose.orientation = robot_pose.orientation
        
        return camera_pose

    def create_point_cloud(self, depth_image: np.ndarray) -> np.ndarray:
        """Create point cloud from depth image"""
        height, width = depth_image.shape
        points = []
        
        for v in range(height):
            for u in range(width):
                z = depth_image[v, u]
                if z > 0:  # Valid depth
                    x = (u - self.cx) * z / self.fx
                    y = (v - self.cy) * z / self.fy
                    points.append([x, y, z])
        
        return np.array(points)

    def visualize_perception_output(self, output: HumanoidPerceptionOutput, image: np.ndarray):
        """Visualize perception results on image"""
        vis_image = image.copy()
        
        # Draw bounding boxes for detected objects
        for detection in output.objects:
            x, y, w, h = detection.bbox
            color = (0, 255, 0) if detection.class_name == 'person' else (255, 0, 0)
            cv2.rectangle(vis_image, (x, y), (x+w, y+h), color, 2)
            
            # Add label
            label = f"{detection.class_name}: {detection.confidence:.2f}"
            cv2.putText(vis_image, label, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Show image
        cv2.imshow('Perception Output', vis_image)
        cv2.waitKey(1)

# Example usage
def main():
    print("Humanoid Perception System")
    print("=" * 35)
    
    # Initialize perception system
    perception = HumanoidPerception()
    
    # Simulate creating test image and depth data
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some colored regions to simulate objects
    cv2.rectangle(test_image, (100, 100), (200, 200), (0, 200, 200), -1)  # Yellow (cup-like)
    cv2.rectangle(test_image, (300, 150), (400, 250), (255, 0, 0), -1)   # Blue (book-like)
    cv2.rectangle(test_image, (200, 300), (300, 400), (0, 150, 200), -1) # Skin tone (person-like)
    
    # Simulate depth image
    depth_image = np.ones((480, 640), dtype=np.float32) * 2.0  # 2 meters away
    depth_image[100:200, 100:200] = 1.5  # Cup closer
    depth_image[300:400, 150:250] = 1.8  # Book distance
    depth_image[200:400, 200:300] = 1.2  # Person closer
    
    # Simulate IMU data
    imu_data = {
        'orientation_x': 0.0,
        'orientation_y': 0.0,
        'orientation_z': 0.1,
        'orientation_w': 0.995,
        'position_x': 0.0,
        'position_y': 0.0,
        'position_z': 0.8
    }
    
    # Process the data
    output = perception.integrate_sensor_data(test_image, depth_image, imu_data)
    
    print(f"Detected {len(output.objects)} objects:")
    for obj in output.objects:
        pos_str = f" at {obj.center_3d}" if obj.center_3d is not None else " (no depth)"
        print(f"  - {obj.class_name} (confidence: {obj.confidence:.2f}){pos_str}")
    
    print(f"Floor normal: {output.floor_normal}")
    print(f"Support polygon: {output.support_polygon}")
    
    # Visualize results
    perception.visualize_perception_output(output, test_image)
    
    print("Perception processing completed!")

if __name__ == "__main__":
    main()
```

## Simulation

### Perception Simulation in Gazebo

Simulating perception systems in Gazebo requires realistic sensor models that accurately replicate real-world sensor characteristics:

1. **Camera Simulation**: Simulate RGB, stereo, and RGB-D cameras with realistic noise and distortion
2. **LiDAR Simulation**: Model beam divergence, multiple returns, and environmental effects
3. **IMU Simulation**: Include sensor bias, drift, and noise characteristics
4. **Force/Torque Simulation**: Add realistic noise and delay to force measurements

### Gazebo Sensor Configuration Example

```xml
<!-- Example: RGB-D camera plugin configuration -->
<gazebo reference="camera_link">
  <sensor name="camera" type="depth">
    <always_on>true</always_on>
    <update_rate>30</update_rate>
    <camera name="head_camera">
      <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees in radians -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>10.0</far>
      </clip>
      <noise>
        <type>gaussian</type>
        <mean>0.0</mean>
        <stddev>0.007</stddev>
      </noise>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_optical_frame</frame_name>
      <min_depth>0.1</min_depth>
      <max_depth>10.0</max_depth>
    </plugin>
  </sensor>
</gazebo>
```

### Perception Simulation Exercises

1. **Object Detection Simulation**:
   - Create various objects in Gazebo with different textures and colors
   - Test your perception algorithms with these simulated objects
   - Evaluate detection accuracy under different lighting conditions

2. **SLAM Validation**:
   - Create a known environment in Gazebo
   - Run SLAM algorithms and compare generated maps with ground truth
   - Analyze the effect of sensor noise on mapping accuracy

3. **Multi-sensor Fusion**:
   - Combine data from multiple simulated sensors (camera, LiDAR, IMU)
   - Implement sensor fusion algorithms and validate in simulation
   - Compare fused results with individual sensor outputs

4. **Dynamic Scene Perception**:
   - Add moving objects to your simulation environment
   - Test object tracking algorithms with dynamic scenes
   - Evaluate perception robustness with occlusions and clutter

## Exercises

1. **Basic Perception Tasks**:
   - Implement a basic object detection pipeline using OpenCV
   - Create a 3D reconstruction from stereo images
   - Develop a simple SLAM system for a mobile robot

2. **Deep Learning Integration**:
   - Train a neural network for object detection in indoor environments
   - Implement semantic segmentation for scene understanding
   - Create a people detection and tracking system

3. **Sensor Fusion Projects**:
   - Implement a Kalman filter to fuse IMU and camera data
   - Create a particle filter for robot localization
   - Develop a system that combines visual and LiDAR data

4. **Humanoid-Specific Challenges**:
   - Implement perception for object affordances (what can be grasped)
   - Create a system for human intention recognition from motion
   - Develop social perception for human-robot interaction

5. **Advanced Perception**:
   - Implement visual-inertial odometry for more accurate localization
   - Create a system for predicting object physics in the environment
   - Develop a perception system that learns from human demonstrations

## Bibliography & Further Reading

1. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications*. Springer.
2. Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press.
3. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
4. OpenCV Documentation: https://docs.opencv.org/
5. ROS Perception Packages: http://wiki.ros.org/perception