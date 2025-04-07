import requests
import time
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, List, Tuple, Optional


app = FastAPI()

class OptitrackStreamReceiver:
    def __init__(self):
        # Position data
        self.position_x = 0.0
        self.position_y = 0.0
        self.position_z = 0.0
        
        # Orientation data as quaternion
        self.q = np.array([1.0, 0.0, 0.0, 0.0])  # [w, x, y, z]
        
        # Orientation in Euler angles (yaw, pitch, roll)
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        
        # Raw marker data
        self.markers = []
        
        # Rigid body data
        self.rigid_body_data = None

    def update_position(self):
        try:
            # TODO: read this from config
            response = requests.get("http://10.42.0.1:5001/Optitracking_data_forward")
            if response.status_code == 200:
                data = response.json()
                self._parse_optitrack_data(data)
                print(f"Updated position: ({self.position_x}, {self.position_y}, {self.position_z})")
                print(f"Orientation (yaw, pitch, roll): ({self.yaw}, {self.pitch}, {self.roll})")
            else:
                print("Failed to update Opti positions")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching robot opti position: {e}")
    
    def _parse_optitrack_data(self, data: Dict[str, Any]) -> None:
        """Parse the received OptiTrack data and update object attributes"""
        opti_data = data.get("Opti_data")
        if opti_data is None or not opti_data:
            print("No OptiTrack data available")
            return
        
        # Get rigid body data - we're using only one rigid body
        rigid_bodies = opti_data.get("rigidbodies", [])
        if rigid_bodies and len(rigid_bodies) > 0:
            self.rigid_body_data = rigid_bodies[0]
            
            # Extract position
            position = self.rigid_body_data.get("position", [0, 0, 0])
            if position and len(position) >= 3:
                self.position_x = position[0]
                self.position_y = position[1]
                self.position_z = position[2]
            
            # Extract quaternion
            quaternion = self.rigid_body_data.get("rotation", [1, 0, 0, 0])
            if quaternion and len(quaternion) >= 4:
                # OptiTrack quaternion format is [x, y, z, w]
                # Convert to [w, x, y, z] format
                #self.q = np.array([quaternion[3], quaternion[0], quaternion[1], quaternion[2]])
                # If OptiTrack is actually sending [w, x, y, z], use this instead:
                self.q = np.array(quaternion)
                
                # Calculate yaw, pitch, roll
                self.yaw, self.pitch, self.roll = self._calculate_yaw_pitch_roll()
            
            # Check tracking validity
            tracking_valid = self.rigid_body_data.get("tracking_valid", False)
            if not tracking_valid:
                print("Warning: OptiTrack reports tracking is not valid")
        else:
            print("No rigid body data available in the response")
    
    def get_position(self) -> Tuple[float, float, float]:
        """Return the current position as (x, y, z)"""
        return self.position_x, self.position_y, self.position_z
    
    def get_orientation(self) -> Tuple[float, float, float]:
        """Return the current orientation as (yaw, pitch, roll)"""
        return self.yaw, self.pitch, self.roll
    
    def get_orientation_yaw(self) -> Tuple[float]:
        """Return the current orientation as (yaw, pitch, roll)"""
        return self.yaw
    
    def get_first_marker_coordinates(self) -> Tuple[float, float]:
        """Return the 2D position (x, z) for ground plane navigation"""
        return self.position_x, self.position_z
    
    def _normalise(self) -> None:
        """Normalize the quaternion to unit length"""
        norm = np.linalg.norm(self.q)
        if norm > 0:
            self.q = self.q / norm
    
    def _calculate_yaw_pitch_roll(self) -> Tuple[float, float, float]:
        """Calculate the yaw, pitch, roll angles from the quaternion"""
        #self._normalise()
        qw = self.q[0]
        qx = self.q[1]
        qy = self.q[2]
        qz = self.q[3]
        
        # Check for gimbal lock cases
        test = 2 * (qx * qz - qw * qy)
        
        if test >= 0.95:  # North pole gimbal lock
            yaw = np.arctan2(qx * qy - qw * qz, qx * qz + qw * qy)
            pitch = np.pi / 2  # 90 degrees
            roll = 0
        elif test <= -0.95:  # South pole gimbal lock
            yaw = -np.arctan2(qx * qy - qw * qz, qx * qz + qw * qy)
            pitch = -np.pi / 2  # -90 degrees
            roll = 0
        else:
            yaw = np.arctan2(2 * (qy * qz + qw * qx), 1 - 2 * (qx**2 + qy**2))
            pitch = np.arcsin(test)
            roll = np.arctan2(2 * (qx * qy + qw * qz), 1 - 2 * (qy**2 + qz**2))
        
        return yaw, pitch, roll

if __name__ == "__main__":
    tracker = OptitrackStreamReceiver()
    while True:
        tracker.update_position()
        x, z = tracker.get_first_marker_coordinates()
        print(f"2D position: ({x}, {z})")
        yaw, pitch, roll = tracker.get_orientation()
        print(f"Orientation (yaw, pitch, roll): ({yaw}, {pitch}, {roll})")
        time.sleep(1)
