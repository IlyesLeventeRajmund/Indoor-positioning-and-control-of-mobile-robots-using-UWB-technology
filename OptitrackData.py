import requests
import time

class RobotLocationOptitrack:
    def __init__(self):
        self.last_positions = []

    def update_position(self):
        try:
            response = requests.get("http://10.42.0.1:5001/Optitracking_data_forward")
            if response.status_code == 200:
                data = response.json()
                new_positions = extract_marker_positions(data)
                if new_positions:
                    self.last_positions = new_positions
                print("Current OptiTrack Positions:", self.last_positions)
            else:
                print("Failed to update Opti positions")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching robot opti position: {e}")

    def get_first_marker_coordinates(self):
        if self.last_positions:
            first_marker = self.last_positions[0]
            position = first_marker.get("position", {})
            if position:
                #print("pozik:", position[0], position[2])
                return position[0], position[2]
        return None, None

            

def extract_marker_positions(data):
    opti_data = data.get("Opti_data")
    if opti_data is None:
        return []  
    markers = opti_data.get("markers", [])
    return [{"id": marker["id"], "position": marker["position"]} for marker in markers]


if __name__ == "__main__":
    tracker = RobotLocationOptitrack()
    while True:
        tracker.update_position()
        tracker.get_first_marker_coordinates()
        time.sleep(1)
