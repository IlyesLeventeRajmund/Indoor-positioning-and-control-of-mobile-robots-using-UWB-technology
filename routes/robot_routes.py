from fastapi import APIRouter
from controller.robot_controller import RobotController
from models.move_input import MoveInput
from models.speed_input import SpeedInput
from models.optitrack_data import OptiTrackData  
from fastapi import HTTPException
import logging

router = APIRouter()
robot_controller = RobotController() 

@router.post("/Optitracking_data")
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
        
@router.get("/Optitracking_data_forward")
async def get_Optitracking_data():
    return {"Opti_data": self.optitrack_data}

@router.post("/speed")
async def make_speed(data: SpeedInput):
    if 0 <= data.speed <= 100:
        self.current_speed = data.speed
        return {"status": "success", "speed": self.current_speed}
    else:
        raise HTTPException(status_code=400, detail="Invalid speed")
        
@router.get("/current_speed")
async def get_current_speed():
    return {"speed": self.current_speed}

@router.post("/move")
async def move_robot(data: MoveInput):
    # # TODO: Move this to base model
    # valid_directions = ['up', 'down', 'left', 'right', 'stop', 'up-left', 
    #                     'up-right', 'down-left', 'down-right', 'circle', 
    #                     'square', 'triangle', 'hexagon']
    
    # TODO: come up with a name for directions

    # if data.direction not in valid_directions:
    #     raise HTTPException(status_code=400, detail="Invalid direction")
    
    # TODO: transfor MoveInput to a usable format
    logging.debug(f"Received direction: {data.direction}")
    robot_controller.set_direction(data.direction)

    return {"status": "success", "direction": data.direction}

# Control mode
@router.post("/controll_mode")
async def set_control_mode(data: ControlMode):
    self.control_mode = data.manual
    return {"status": "success", "manual": self.control_mode}

@router.get("/controll_mode")
async def get_control_mode():
    return {"manual": self.control_mode}

# point
@router.post("/point")
async def update_point(data: PointData):
    self.point = data.dict()
    return {"status": "success", "point": self.point}

@router.get("/point")
async def get_point():
    if self.point is None:
        raise HTTPException(status_code=404, detail="No point data")
    return self.point

# Circle
@router.post("/circle")
async def update_circle(data: CircleData):
    self.circle = data.dict()
    return {"status": "success", "circle": self.circle}

@router.get("/circle")
async def get_circle():
    if self.circle is None:
        raise HTTPException(status_code=404, detail="No circle data")
    return self.circle


# @router.get("/current_direction")
# async def get_current_direction():
#     return {"direction": self.current_direction}

# @router.delete("/clear")
# async def clear_locations():
#     try:
#         # Any clearing logic needed
#         return {"status": "success"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/beacons")
# async def get_beacon_positions():
#     return robot.device_positions

# @router.post("/beacons")
# async def update_beacon_positions(data: BeaconData):
#     self.device_positions = {
#         "DC:C7:ED:2C:04:D1": (data.beacon1["x"], data.beacon1["y"]),
#         "D1:DC:74:F2:C7:05": (data.beacon2["x"], data.beacon2["y"]),
#         "D0:FB:A6:16:7D:AC": (data.beacon3["x"], data.beacon3["y"]),
#         "C3:F0:97:50:8B:EA": (data.beacon4["x"], data.beacon4["y"])
#     }
#     return {"status": "success"}

# @router.post("robot/position")
# async def receive_position(data: Location):
#     self.location["x"] = data.x
#     self.location["y"] = data.y
#     return {"message": "Location data saved"}

# @router.get("/locations")
# async def get_locations():
#     return self.location

# @router.post("/distance")
# async def receive_distance(data: DistanceInput):
#     if data.distance >= 0:
#         self.current_distance = data.distance
#         return {"status": "success", "distance": self.current_distance}
#     else:
#         raise HTTPException(status_code=400, detail="Invalid distance")

# @router.get("/current_distance")
# async def get_current_distance():
#     if robot_controller.get_distance is not None:
#         return {"distance": self.current_distance}
#     else:
#         raise HTTPException(status_code=400, detail="No distance recorded")