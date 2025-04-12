from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import logging

class Location(BaseModel):
    x: float
    y: float
    timestamp: Optional[datetime] = None

class BeaconData(BaseModel):
    beacon1: Dict[str, float]
    beacon2: Dict[str, float]
    beacon3: Dict[str, float]
    beacon4: Dict[str, float]

class OptiTrackData(BaseModel):
    data: str

class OptiTrackMarkerData(BaseModel):
    data: str
    
class SpeedInput(BaseModel):
    speed: float
    
class MoveInput(BaseModel):
    direction: str
    
class DistanceInput(BaseModel):
    distance: float

class RobotServer:
    def __init__(self, host="0.0.0.0", port=5001):

        logging.getLogger("uvicorn.access").disabled = True
        logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

        self.app = FastAPI()
        self.host = host
        self.port = port
        self.thread = None
        self.server = None
        
        # State variables
        self.location = {}
        self.current_direction = None
        self.current_speed = 50
        self.current_distance = None
        self.optitrack_data = None
        self.optitrack_marker_data = None
        self.device_positions = {}
        
        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Register routes
        self._setup_routes()
        
    def _setup_routes(self):
        # Optitrack data routes
        @self.app.post("/Optitracking_marker_data")
        async def receive_Optitracking_marker_data(data: OptiTrackMarkerData):
            if not data.data:
                raise HTTPException(status_code=400, detail="Invalid data")
            self.optitrack_marker_data = data.data
            return {"status": "success", "Opti Location": self.optitrack_marker_data}
        
        @self.app.get("/Optitracking_marker_data_forward")
        async def get_Optitracking_marker_data():
            return {"Opti_data": self.optitrack_marker_data}

        @self.app.post("/Optitracking_data")
        async def receive_Optitracking_data(data: OptiTrackData):
            if not data.data:
                raise HTTPException(status_code=400, detail="Invalid data")
            
            # Parse the incoming data string and store in structured format
            raw_data = data.data
            #print(f"Received data: {raw_data}")
            
            # Parse the data string to extract rigid body information
            parsed_data = {}
            
            # Check if there's a rigid body in the data
            if "Rigid Body Count:" in raw_data:
                # Extract position
                position_match = raw_data.find("Position      :")
                if position_match != -1:
                    pos_str = raw_data[position_match:].split("\n")[0]
                    pos_values = pos_str.split("[")[1].split("]")[0].split(",")
                    position = [float(p.strip()) for p in pos_values]
                    parsed_data["position"] = position
                
                # Extract orientation
                orientation_match = raw_data.find("Orientation   :")
                if orientation_match != -1:
                    orient_str = raw_data[orientation_match:].split("\n")[0]
                    orient_values = orient_str.split("[")[1].split("]")[0].split(",")
                    orientation = [float(o.strip()) for o in orient_values]
                    parsed_data["rotation"] = orientation
                
                # Store tracking validity
                tracking_valid = "Tracking Valid: True" in raw_data
                parsed_data["tracking_valid"] = tracking_valid
                
                # Structure the data in a format the client expects
                self.optitrack_data = {
                    "rigidbodies": [parsed_data],
                    "markers": []
                }
    
            return {"status": "success", "Opti Location": data.data}
        
        @self.app.get("/Optitracking_data_forward")
        async def get_Optitracking_data():
            return {"Opti_data": self.optitrack_data}
        
        # Speed routes
        @self.app.post("/speed")
        async def make_speed(data: SpeedInput):
            if 0 <= data.speed <= 100:
                self.current_speed = data.speed
                return {"status": "success", "speed": self.current_speed}
            else:
                raise HTTPException(status_code=400, detail="Invalid speed")
        
        @self.app.get("/current_speed")
        async def get_current_speed():
            return {"speed": self.current_speed}
        
        # Movement routes
        @self.app.post("/move")
        async def move_robot(data: MoveInput):
            valid_directions = ['up', 'down', 'left', 'right', 'stop', 'up-left', 
                               'up-right', 'down-left', 'down-right', 'circle', 
                               'square', 'triangle', 'hexagon']
            if data.direction not in valid_directions:
                raise HTTPException(status_code=400, detail="Invalid direction")
            self.current_direction = data.direction
            return {"status": "success", "direction": self.current_direction}
        
        @self.app.get("/current_direction")
        async def get_current_direction():
            return {"direction": self.current_direction}
        
        # Clear route
        @self.app.delete("/clear")
        async def clear_locations():
            try:
                # Any clearing logic needed
                return {"status": "success"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        # Beacon routes
        @self.app.get("/beacons")
        async def get_beacon_positions():
            return self.device_positions
        
        @self.app.post("/beacons")
        async def update_beacon_positions(data: BeaconData):
            self.device_positions = {
                "DC:C7:ED:2C:04:D1": (data.beacon1["x"], data.beacon1["y"]),
                "D1:DC:74:F2:C7:05": (data.beacon2["x"], data.beacon2["y"]),
                "D0:FB:A6:16:7D:AC": (data.beacon3["x"], data.beacon3["y"]),
                "C3:F0:97:50:8B:EA": (data.beacon4["x"], data.beacon4["y"])
            }
            return {"status": "success"}
        
        # Position routes
        @self.app.post("/position")
        async def receive_position(data: Location):
            self.location["x"] = data.x
            self.location["y"] = data.y
            return {"message": "Location data saved"}
        
        @self.app.get("/locations")
        async def get_locations():
            return self.location
        
        # Distance routes
        @self.app.post("/distance")
        async def receive_distance(data: DistanceInput):
            if data.distance >= 0:
                self.current_distance = data.distance
                return {"status": "success", "distance": self.current_distance}
            else:
                raise HTTPException(status_code=400, detail="Invalid distance")
        
        @self.app.get("/current_distance")
        async def get_current_distance():
            if self.current_distance is not None:
                return {"distance": self.current_distance}
            else:
                raise HTTPException(status_code=400, detail="No distance recorded")
    
    def start(self):
        """Start the server in a separate thread"""
        self.thread = threading.Thread(target=self._run_server)
        self.thread.daemon = True  # Thread will exit when main program exits
        self.thread.start()
        print(f"Server started on http://{self.host}:{self.port}")
        return self.thread
    
    def _run_server(self):
        """Internal method to run the server"""
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="warning")
    
    def stop(self):
        """Stop the server - note: this is not fully implemented as uvicorn doesn't 
        provide a clean shutdown method when run this way"""
        # This is a placeholder - proper shutdown would need a more complex approach
        # with uvicorn's server instance
        if self.thread:
            print("Warning: Cannot fully stop uvicorn server once started.")
            print("You may need to restart your application to fully release the port.")
            
    # Methods to access server data directly from control code
    def get_current_location(self):
        return self.location
    
    def get_direction(self):
        return self.current_direction
    
    def set_direction(self, direction):
        valid_directions = ['up', 'down', 'left', 'right', 'stop', 'up-left', 
                           'up-right', 'down-left', 'down-right', 'circle', 
                           'square', 'triangle', 'hexagon']
        if direction not in valid_directions:
            raise ValueError("Invalid direction")
        self.current_direction = direction
        
    def get_speed(self):
        return self.current_speed
    
    def set_speed(self, speed):
        if 0 <= speed <= 100:
            self.current_speed = speed
        else:
            raise ValueError("Invalid speed")
            
    def get_distance(self):
        return self.current_distance
    
    def set_distance(self, distance):
        if distance >= 0:
            self.current_distance = distance
        else:
            raise ValueError("Invalid distance")
    
    def get_optitrack_data(self):
        return self.optitrack_data
    
    def get_beacon_positions(self):
        return self.device_positions