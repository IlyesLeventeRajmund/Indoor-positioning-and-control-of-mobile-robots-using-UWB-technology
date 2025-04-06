

class Robot:
    def __init__(self):
        self.location = {}
        self.current_direction = None
        self.current_speed = 50
        self.current_distance = None
        self.optitrack_data = None
        self.device_positions = {}

    def get_current_location(self):
        return self.location
    
    def get_direction(self):
        return self.current_direction
    
    def set_direction(self, direction):
        # This should not be in a class method
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