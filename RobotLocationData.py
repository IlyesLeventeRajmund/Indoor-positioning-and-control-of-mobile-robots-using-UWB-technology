import requests
import time

class RobotLocationBeacon:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def set_coordinates(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y
    
    def update_position(self):
        try:
            response = requests.get("http://10.42.0.1:5001/locations")
            if response.status_code == 200:
                data = response.json()
                if 'x' in data and 'y' in data:
                    self.set_coordinates(data['x'], data['y'])
                print("Current Beacon Position:", self.get_coordinates())
            else:
                print("Failed to update Beacon position")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching beacon position: {e}")

if __name__ == "__main__":
    tracker = RobotLocationBeacon(0,0)
    while True:
        tracker.update_position()
        time.sleep(1)