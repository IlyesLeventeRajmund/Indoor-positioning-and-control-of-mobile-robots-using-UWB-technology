from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

location = {}
current_direction = None
current_speed = 50
current_distance = None
optitrack_data = None
device_positions = {}

class Location(BaseModel):
    x: float
    y: float
    timestamp: Optional[datetime] = None

class BeaconData(BaseModel):
    beacon1: Dict[str, float]
    beacon2: Dict[str, float]
    beacon3: Dict[str, float]
    beacon4: Dict[str, float]

@app.post("/Optitracking_data")
async def reciev_Optitracking_data(data: dict):
    global optitrack_data
    if not data.get("data"):
        raise HTTPException(status_code=400, detail="Invalid data")
    optitrack_data = data["data"]
    return {"status": "success", "Opti Location": optitrack_data}

@app.get("/Optitracking_data_forward")
async def get_Optitracking_data():
    return {"Opti_data": optitrack_data}

@app.post("/speed")
async def make_speed(speed: float):
    global current_speed
    if isinstance(speed, (int, float)) and speed <= 100:
        current_speed = speed
        return {"status": "success", "speed": current_speed}
    else:
        raise HTTPException(status_code=400, detail="Invalid speed")

@app.get("/current_speed")
async def get_current_speed():
    return {"speed": current_speed}

@app.post("/move")
async def move_robot(direction: str):
    global current_direction
    valid_directions = ['up', 'down', 'left', 'right', 'stop', 'up-left', 'up-right', 'down-left', 'down-right', 'circle', 'square', 'triangle', 'hexagon']
    if direction not in valid_directions:
        raise HTTPException(status_code=400, detail="Invalid direction")
    current_direction = direction
    return {"status": "success", "direction": current_direction}

@app.get("/current_direction")
async def get_current_direction():
    return {"direction": current_direction}

@app.delete("/clear")
async def clear_locations():
    try:
        # Assuming db setup for deletion is needed, e.g., db.session.query(Location).delete()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/beacons")
async def get_beacon_positions():
    return device_positions

@app.post("/beacons")
async def update_beacon_positions(data: BeaconData):
    global device_positions
    device_positions = {
        "DC:C7:ED:2C:04:D1": (data.beacon1["x"], data.beacon1["y"]),
        "D1:DC:74:F2:C7:05": (data.beacon2["x"], data.beacon2["y"]),
        "D0:FB:A6:16:7D:AC": (data.beacon3["x"], data.beacon3["y"]),
        "C3:F0:97:50:8B:EA": (data.beacon4["x"], data.beacon4["y"])
    }
    return {"status": "success"}

@app.post("/position")
async def receive_position(data: Location):
    x = data.x
    y = data.y
    location["x"] = x
    location["y"] = y
    return {"message": "Location data saved"}

@app.get("/locations")
async def get_locations():
    return location

@app.post("/distance")
async def receive_distance(distance: float):
    global current_distance
    if isinstance(distance, (int, float)) and distance >= 0:
        current_distance = distance
        return {"status": "success", "distance": current_distance}
    else:
        raise HTTPException(status_code=400, detail="Invalid distance")

@app.get("/current_distance")
async def get_current_distance():
    if current_distance is not None:
        return {"distance": current_distance}
    else:
        raise HTTPException(status_code=400, detail="No distance recorded")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
