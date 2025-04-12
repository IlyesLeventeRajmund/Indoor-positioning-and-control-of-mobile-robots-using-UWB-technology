import RPi.GPIO as GPIO
from time import time
from time import sleep
from datetime import datetime
import numpy as np
import json
import threading
import OptitrackData
import BeaconLocalization
import ManualModeData
import random
import math
from appFastapi import RobotServer  # Import the server class we created
import atexit

def gpioInit():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)

    pwm1 = GPIO.PWM(22, 1000)  
    pwm2 = GPIO.PWM(17, 1000) 
    pwm3 = GPIO.PWM(16, 1000)
    pwm4 = GPIO.PWM(21, 1000)
    pwm5 = GPIO.PWM(23, 1000) 
    pwm6 = GPIO.PWM(27, 1000)  
    pwm7 = GPIO.PWM(12, 1000) 
    pwm8 = GPIO.PWM(26, 1000)  

    pwm1.start(0)
    pwm2.start(0)
    pwm3.start(0)
    pwm4.start(0)
    pwm5.start(0)
    pwm6.start(0)
    pwm7.start(0)
    pwm8.start(0)

    atexit.register(safe_cleanup, [pwm1, pwm2, pwm3, pwm4, pwm5, pwm6, pwm7, pwm8])

    return pwm1, pwm2, pwm3, pwm4, pwm5, pwm6, pwm7, pwm8

def safe_cleanup(pwm_list):
    """Safely clean up GPIO resources while avoiding lgpio errors"""
    try:
        # First set all duty cycles to 0
        for p in pwm_list:
            try:
                p.ChangeDutyCycle(0)
            except:
                pass
        
        # Then explicitly set all pins to input mode rather than calling stop()
        pins = [22, 23, 17, 27, 12, 16, 20, 21]
        for pin in pins:
            try:
                GPIO.setup(pin, GPIO.IN)
            except:
                pass
        
        # Call cleanup but catch any exceptions
        try:
            GPIO.cleanup()
        except:
            pass
    except Exception as e:
        print(f"Error during safe cleanup: {e}")

def main():
    # Initialize the FastAPI server in a separate thread
    print("Initializing FastAPI server...")
    robot_server = RobotServer(host="0.0.0.0", port=5001)
    server_thread = robot_server.start()

    # Initialize GPIO
    print("Initializing GPIO...")
    pwm = gpioInit()

    # Initialize and start OptiTracker
    print("Initializing OptiTracker...")
    OptiTracker = OptitrackData.RobotLocationOptitrack()
    
    # Initialize and start BeaconTracker in a separate thread
    print("Initializing and starting BeaconTracker...")
    BeaconTracker = BeaconLocalization.RobotLocationBeacon(0, 0)
    BeaconTracker.start_tracking()  # This starts its own thread
    
    start_time = time()

    # Define Robot Parameters
    L1 = 0.06  # Distance between the center and the wheels (meters)
    L2 = 0.07
    R = 0.03  # Radius of the wheels (meters)
    Kp = 1.5  # Proportional gain for velocity control
    Kd = 1  # Derivative gain for velocity control

    Pr = (1, 1)

    wheel_positions = np.array([
        [L2, L1],   # Jobb első kerék
        [-L2, L1],  # Bal első kerék
        [-L2, -L1], # Bal hátsó kerék
        [L2, -L1],  # Jobb hátsó kerék
    ])


    def wheel_velocity_transform(vx, vy, w):
        wheel_velocities = np.array([
            
            (1/R) * (vx + vy + (L1+L2) * w),  # Jobb hátsó kerék
            (1/R) * (vx - vy + (L1+L2) * w),  # Jobb első kerék
            (1/R) * (vx - vy - (L1+L2) * w),  # Bal hátsó kerék
            (1/R) * (vx + vy - (L1+L2) * w),  # Bal első kerék

            #(1/R) * (-vx - vy - (L1+L2) * w),  # Jobb hátsó kerék
            #(1/R) * (-vx - vy - (L1+L2) * w),  # Jobb első kerék
            #(1/R) * (-vx - vy + (L1+L2) * w),  # Bal hátsó kerék
            #(1/R) * (-vx - vy + (L1+L2) * w),  # Bal első kerék

            #(1/R) * (+vx + vy - (L1+L2) * w),  # Jobb hátsó kerék
            #(1/R) * (-vx + vy - (L1+L2) * w),  # Jobb első kerék
            #(1/R) * (-vx + vy + (L1+L2) * w),  # Bal hátsó kerék
            #(1/R) * (+vx + vy + (L1+L2) * w),  # Bal első kerék

        ])
        print("vx:", vx)
        print("vy:", vy)
        return wheel_velocities

    def p_control(current_pose, desired_pose, current_teta, desired_teta):
        error_x = desired_pose[0] - current_pose[0]
        error_y = desired_pose[1] - current_pose[1]
        error_theta = desired_teta - current_teta
        
        vx_world = Kp * error_x
        vy_world = Kp * error_y
        w = 0#Kd * error_theta

        vx= math.cos(current_teta)*vx_world +math.sin(current_teta)*vy_world
        vy = -math.sin(current_teta)*vx_world + math.cos(current_teta)*vy_world
        
        #print("error",error_x,error_y,error_theta)
        print("szog",current_teta)
        #print("elvart",desired_pose[0])
        #print("jelenlegi",current_pose[0])

        return vx, vy, w

    def automat_control(Pc, Pr, Tc, Tr):
        vx, vy, w = p_control(Pc, Pr, Tc, Tr)

        wheel_speeds = wheel_velocity_transform(vy, vx, w)
        duty_start = 20
        for i, pwm_forward, pwm_backward in zip(range(4), [pwm[0], pwm[1], pwm[2], pwm[3]], [pwm[4], pwm[5], pwm[6], pwm[7]]):
            if wheel_speeds[i] > 0:
                duty = max(0, min(100, abs(wheel_speeds[i]+duty_start)))
                
                pwm_forward.ChangeDutyCycle(0)
                pwm_backward.ChangeDutyCycle(duty)
                
            else:
                duty = max(0, min(100, abs(wheel_speeds[i]+duty_start)))
                
                pwm_forward.ChangeDutyCycle(duty)
                pwm_backward.ChangeDutyCycle(0)

    def shapeGenerator(shape, size, num_points):
        points = []
        
        if shape == 'circle':
            radius = math.sqrt(size)
            for _ in range(num_points):
                angle = random.uniform(0, 2 * math.pi)
                r = random.uniform(0, radius)
                x = r * math.cos(angle)
                y = r * math.sin(angle)
                points.append((x, y))
        
        elif shape == 'triangle':
            for _ in range(num_points):
                x = random.uniform(0, size)
                y = random.uniform(0, (size * math.sqrt(3)) / 2)
                if y > (math.sqrt(3) * x) or y > (-math.sqrt(3) * x + size * math.sqrt(3)):
                    continue
                points.append((x, y))
        
        elif shape == 'hexagon':
            for _ in range(num_points):
                angle = random.randint(0, 5) * math.pi / 3
                r = random.uniform(0, size)
                x = r * math.cos(angle)
                y = r * math.sin(angle)
                points.append((x, y))
        
        elif shape == 'square':
            for _ in range(num_points):
                x = random.uniform(-size / 2, size / 2)
                y = random.uniform(-size / 2, size / 2)
                points.append((x, y))
        
        return points

    LOG_FILE = "log.json"

    def calculate_2d_distance(pos1, pos2):
        return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

    def log_beacon_data(beacon_data, optitrack_position, beacon_positions):
        target_macs = ["D1:DC:74:F2:C7:05", "D0:FB:A6:16:7D:AC", "EC:7F:50:BE:D2:D1"]

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "beacons": [],
        }

        print("Beacon data:", beacon_data)

        if not beacon_data:
            print("Beacon data is empty.")

        for target_mac in target_macs:
            beacon_info = beacon_data.get(target_mac)
            if beacon_info and all(k in beacon_info for k in ("rssi", "distance")):
                beacon_position = beacon_positions.get(target_mac)
                if beacon_position:
                    distance_optitrack = calculate_2d_distance(optitrack_position, beacon_position)
                    beacon_entry = {
                        "id": target_mac,
                        "rssi": beacon_info["rssi"],
                        "calculated_distance": beacon_info["distance"],
                        "distance_from_optitrack": distance_optitrack
                    }
                    log_entry["beacons"].append(beacon_entry)

        if not log_entry["beacons"]:
            print("No beacons to log.")

        with open(LOG_FILE, "a") as f:
            json.dump(log_entry, f)
            f.write("\n")





    # This replaces the HTTP request with direct access to the server data
    def direction_call():
        direction = robot_server.get_direction()
        speed = robot_server.get_speed()
        #print("az irany:", direction)
        #print("a sebesseg:", speed)
        return speed, direction

    # Initialize path variables
    circle_path = None
    square_path = None
    triangle_path = None
    hexagon_path = None
    count = 0

    try:
        print("Main control loop starting...")
        while True:
            # delay 10ms
            sleep(0.1)  # 100ms
            
            beacon_positions = {
                "DC:C7:ED:2C:04:D1": (1.9146842956542969, -0.40974411368370056),
                "D1:DC:74:F2:C7:05": (-0.12133240699768066, -3.605344772),
                "D0:FB:A6:16:7D:AC": (1.2901723384857178, -2.0813114643096924),
                "C3:F0:97:50:8B:EA": (-1.4125473499298096, -0.4882330298423767),
                "EC:7F:50:BE:D2:D1": (-1.2612544298171997, -1.9906595945358276),
                "C0-0B-BD-29-25-9C": (1.9020336866378784, 1.0856691598892212),
                "DA-53-A2-B5-96-75": (0.45428064465522766, 1.9725672006607056),
                "D6-7E-98-FA-DE-01": (-1.4703487157821655, 1.0286478996276855)
            }

            OptiTracker.update_position()
            Po = OptiTracker.get_first_marker_coordinates()
            # BeaconTracker updates in its own thread, so we just need to get the coordinates
            Pb = BeaconTracker.get_coordinates()

            Po = (Po[0] if Po[0] is not None else 0.0, Po[1] if Po[1] is not None else 0.0)
            Pb = (Pb[0] if Pb[0] is not None else 0.0, Pb[1] if Pb[1] is not None else 0.0)

            print(f"DEBUG - Po: {Po}, Pb: {Pb}")
            Beacon_data = BeaconTracker.get_all_beacon_distances()
            print("Beacon adatok:",Beacon_data)
            log_beacon_data(Beacon_data, Po, beacon_positions)

            # Update the server with the position data
            if Po[0] is not None and Po[1] is not None:
                robot_server.location = {"x": Po[0], "y": Po[1]}
            
            E = (Po[0] - Pb[0], Po[1] - Pb[1])

            elapsed_time = time() - start_time

            log_data = {
                'timestamp': f"{elapsed_time:.6f}",
                'Pr': Pr,
                'Po': Po,
                'Pb': Pb,
                'ERROR': E
            }
            
            with open('robot_log.json', 'a') as log_file:
                json.dump(log_data, log_file)
                log_file.write("\n")
            
            measure_mode = "Optitrack"
            manual_mode = True

            if measure_mode == 'Beacon':
                Pc = Pb
            else:
                Pc = Po

            Tc = OptiTracker.get_orientation_yaw()
            #teszt = OptiTracker.get_orientation()
            #print("orientaciok:",teszt)
            #print("Tc",Tc)
            Tr = math.atan2(Pr[1] - Pc[1], Pr[0] - Pc[0])

            #print("Tr",Tr)
            # Get direction and speed directly from the server instance
            speed, direction = direction_call()

            if direction:
                if manual_mode:
                    ManualModeData.Manual_Controling(pwm, direction, speed)
                else:
                    if direction == 'stop':
                        for i in range(8):
                            pwm[i].ChangeDutyCycle(0)
                            
                    elif direction == 'circle':
                        if not circle_path:
                            circle_path = shapeGenerator('circle', 1, 12)
                            count = 0
                        
                        Pr = (0,0) #circle_path[count]
                        count = (count + 1) % len(circle_path)
                        automat_control(Pc, Pr, Tc, Tr)
                        
                    elif direction == 'square':
                        if not square_path:
                            square_path = shapeGenerator('square', 1, 12)
                            count = 0

                        Pr = square_path[count]
                        count = (count + 1) % len(square_path)
                        automat_control(Pc, Pr, Tc, Tr)

                    elif direction == 'triangle':
                        if not triangle_path:
                            triangle_path = shapeGenerator('triangle', 1, 12)
                            count = 0

                        Pr = triangle_path[count]
                        count = (count + 1) % len(triangle_path)
                        automat_control(Pc, Pr, Tc, Tr)

                    elif direction == 'hexagon':
                        if not hexagon_path:
                            hexagon_path = shapeGenerator('hexagon', 1, 12)
                            count = 0

                        Pr = hexagon_path[count]
                        count = (count + 1) % len(hexagon_path)
                        automat_control(Pc, Pr, Tc, Tr)
            else:
                sleep(1)
                
    except KeyboardInterrupt:
        print("Program terminated by user")
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        print("Cleaning up resources...")
        # Stop the BeaconTracker
        #BeaconTracker.stop_tracking()
        
        # Don't call pwm[i].stop() here anymore - that's handled by the atexit handler
        # Just set duty cycles to 0 as a precaution
        for i in range(8):
            try:
                pwm[i].ChangeDutyCycle(0)
            except:
                pass
        
        print("Resources cleaned up")

if __name__ == "__main__":
    main()