from controller.robot_low_level_control import initialize_gpio, set_pwm_for_manual_control
from controller.beacon_localization import BeaconLocalization
from controller.optitrack_stream_receiver import OptitrackStreamReceiver

import logging

class RobotController:
    def __init__(self):
        self.location = {}
        self.current_direction = None
        self.current_speed = 50
        self.current_distance = None
        self.optitrack_data = None
        self.device_positions = {}

        print("Initializing GPIO...")
        self.pwms = initialize_gpio()

        self.beacon_localization = BeaconLocalization(0, 0)
        self.beacon_localization.start_tracking()  # This starts its own thread

        # TODO: stop
        # beacon_localization.stop_tracking()

        self.optitrack_stream_receiver = OptitrackStreamReceiver()
        # TODO: stop
        # optitrack_stream_receiver.stop_streaming()
    
    def get_current_location(self):
        return self.location
    
    def get_direction(self):
        return self.current_direction
    
    def set_direction(self, direction):
        # This should not be in a class method
        # TODO: this is duplicated in the routes
        valid_directions = ['up', 'down', 'left', 'right', 'stop', 'up-left', 
                           'up-right', 'down-left', 'down-right', 'circle', 
                           'square', 'triangle', 'hexagon']
                
        if direction not in valid_directions:
            raise ValueError("Invalid direction")
        
        self.current_direction = direction

        # TODO: implement direction here
        # TODO: handle manual or predifined control
        # the result is current_direction and current_speed
        logging.info("Setting direction to: %s", self.current_direction)
        # print("Setting direction to:", self.current_direction)
        # print("Setting speed to:", self.current_speed)
        set_pwm_for_manual_control(
            pwm=self.pwms,
            direction=self.current_direction,
            speed=self.current_speed)

    def get_speed(self):
        return self.current_speed
    
    def set_speed(self, speed):
        if 0 <= speed <= 100:
            self.current_speed = speed
        else:
            raise ValueError("Invalid speed")

        # TODO: implement speed here 

    # def get_distance(self):
    #     return self.current_distance
    
    # def set_distance(self, distance):
        if distance >= 0:
            self.current_distance = distance
        else:
            raise ValueError("Invalid distance")
    
    def get_optitrack_data(self):
        return self.optitrack_data
    
    def get_beacon_positions(self):
        return self.device_positions
    
