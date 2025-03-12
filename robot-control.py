import RPi.GPIO as GPIO
from time import time as current_time
from time import sleep
from datetime import datetime
import requests
import numpy as np
import json
import OptitrackData
import RobotLocationData
import random
import math

OptiTracker = OptitrackData.RobotLocationOptitrack()
BeaconTracker = RobotLocationData.RobotLocationBeacon(0,0)



# Define Robot Parameters
L1 = 0.06  # Distance between the center and the wheels (meters)
L2 = 0.07
R = 0.03  # Radius of the wheels (meters)
Kp = 1.0  # Proportional gain for velocity control
Kd = 0.1  # Derivative gain for velocity control

wheel_positions = np.array([
    [ L2,  L1],  # Jobb első kerék
    [-L2,  L1],  # Bal első kerék
    [-L2, -L1],  # Bal hátsó kerék
    [ L2, -L1],  # Jobb hátsó kerék
])

def wheel_velocity_transform(vx, vy, w):
    wheel_velocities = np.array([
        (1/R) * (vx - vy - L2 * w),  # Jobb első kerék
        (1/R) * (vx + vy + L2 * w),  # Bal első kerék
        (1/R) * (vx + vy - L1 * w),  # Bal hátsó kerék
        (1/R) * (vx - vy + L1 * w),  # Jobb hátsó kerék
    ])
    return wheel_velocities

def p_control(current_pose, desired_pose):
    error_x = desired_pose[0] - current_pose[0]
    error_y = desired_pose[1] - current_pose[1]
    error_theta = 0 #desired_pose[2] - current_pose[2]
    
    vx = Kp * error_x
    vy = Kp * error_y
    w = Kd * error_theta
    
    return vx, vy, w

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

try:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)

    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)

    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)

    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)

    pwm1 = GPIO.PWM(22, 1000)  
    pwm2 = GPIO.PWM(17, 1000) 
    pwm3 = GPIO.PWM(16, 1000)
    pwm4 = GPIO.PWM(21, 1000)

    pwm5 = GPIO.PWM(23, 1000) 
    pwm6 = GPIO.PWM(27, 1000)  
    pwm7 = GPIO.PWM(12, 1000) 
    pwm8 = GPIO.PWM(20, 1000)  

    pwm1.start(0)
    pwm2.start(0)
    pwm3.start(0)
    pwm4.start(0)

    pwm5.start(0)
    pwm6.start(0)
    pwm7.start(0)
    pwm8.start(0)

    while True:
        # Your loop logic here
        pass

except Exception as e:
    print("Hiba történt:", e)

finally:
    GPIO.cleanup()

      
while True:
        #delay 10ms
        sleep(0.1) #100ms
        #megmerni a teljes ciklus idot

        Pr = (0,0)
        OptiTracker.update_position()
        Po = OptiTracker.get_first_marker_coordinates()
        BeaconTracker.update_position()
        Pb = BeaconTracker.get_coordinates()

        log_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Pr': Pr,
            'Po': Po,
            'Pb': Pb
        }
        """
        with open('robot_log.json', 'a') as log_file:
            json.dump(log_data, log_file)
            log_file.write("\n")"""
        
        with open('robot_log.json', 'r') as log_file:
            old_content = log_file.read()

        with open('robot_log.json', 'w') as log_file:
            json.dump(log_data, log_file)
            log_file.write("\n")
            log_file.write(old_content)

        measure_mode = "Beacon"

        if measure_mode =='Beacon':
            Pc = Pb
        else:
            Pc = Po

        direction_response = requests.get('http://10.42.0.1:5001/current_direction')
        speed_response = requests.get('http://10.42.0.1:5001/current_speed')
        print("az irany:",direction_response.json().get("direction"))
        print("a sebesseg:",speed_response.json().get("speed"))

        if direction_response.ok:

            direction = direction_response.json().get("direction")
            speed = speed_response.json().get("speed")

            if direction == 'up':
                #hatra
                pwm1.ChangeDutyCycle(0)   #jh
                pwm2.ChangeDutyCycle(0)   #je
                pwm3.ChangeDutyCycle(0)   #bh
                pwm4.ChangeDutyCycle(0)   #be

                #elore
                pwm5.ChangeDutyCycle(speed)  #jh
                pwm6.ChangeDutyCycle(speed)  #je
                pwm7.ChangeDutyCycle(speed)  #bh
                pwm8.ChangeDutyCycle(speed)  #be
            elif direction == 'down':
                pwm1.ChangeDutyCycle(speed)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(speed)
                pwm4.ChangeDutyCycle(speed)

                pwm5.ChangeDutyCycle(0)
                pwm6.ChangeDutyCycle(0)
                pwm7.ChangeDutyCycle(0)
                pwm8.ChangeDutyCycle(0)
            elif direction == 'left':
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(speed)
                pwm4.ChangeDutyCycle(0)

                pwm5.ChangeDutyCycle(speed)
                pwm6.ChangeDutyCycle(0)
                pwm7.ChangeDutyCycle(0)
                pwm8.ChangeDutyCycle(speed)
            elif direction == 'right':
                pwm1.ChangeDutyCycle(speed)
                pwm2.ChangeDutyCycle(0)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(speed)

                pwm5.ChangeDutyCycle(0)
                pwm6.ChangeDutyCycle(speed)
                pwm7.ChangeDutyCycle(speed)
                pwm8.ChangeDutyCycle(0)
            elif direction == 'stop' :
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(0)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(0)

                pwm5.ChangeDutyCycle(0)
                pwm6.ChangeDutyCycle(0)
                pwm7.ChangeDutyCycle(0)
                pwm8.ChangeDutyCycle(0)
            if direction == 'up-left':
                #hatra
                pwm1.ChangeDutyCycle(0)   #jh
                pwm2.ChangeDutyCycle(0)   #je
                pwm3.ChangeDutyCycle(0)   #bh
                pwm4.ChangeDutyCycle(0)   #be

                #elore
                pwm5.ChangeDutyCycle(speed)  #jh
                pwm6.ChangeDutyCycle(0)  #je
                pwm7.ChangeDutyCycle(0)  #bh
                pwm8.ChangeDutyCycle(speed)  #be
            elif direction == 'up-right':
                #hatra
                pwm1.ChangeDutyCycle(0)   #jh
                pwm2.ChangeDutyCycle(0)   #je
                pwm3.ChangeDutyCycle(0)   #bh
                pwm4.ChangeDutyCycle(0)   #be

                #elore
                pwm5.ChangeDutyCycle(0)  #jh
                pwm6.ChangeDutyCycle(speed)  #je
                pwm7.ChangeDutyCycle(speed)  #bh
                pwm8.ChangeDutyCycle(0)  #be
            elif direction == 'down-left':
                #hatra
                pwm1.ChangeDutyCycle(0)   #jh
                pwm2.ChangeDutyCycle(speed)   #je
                pwm3.ChangeDutyCycle(speed)   #bh
                pwm4.ChangeDutyCycle(0)   #be

                #elore
                pwm5.ChangeDutyCycle(0)  #jh
                pwm6.ChangeDutyCycle(0)  #je
                pwm7.ChangeDutyCycle(0)  #bh
                pwm8.ChangeDutyCycle(0)  #be
            elif direction == 'down-right':
                #hatra
                pwm1.ChangeDutyCycle(speed)   #jh
                pwm2.ChangeDutyCycle(0)   #je
                pwm3.ChangeDutyCycle(0)   #bh
                pwm4.ChangeDutyCycle(speed)   #be

                #elore
                pwm5.ChangeDutyCycle(0)  #jh
                pwm6.ChangeDutyCycle(0)  #je
                pwm7.ChangeDutyCycle(0)  #bh
                pwm8.ChangeDutyCycle(0)  #be
            elif direction == 'circle':
                if not circle_path:
                    circle_path = shapeGenerator('circle', 1, 12)
                count = 0
                Pr = circle_path[count]
                count += 1
                vx, vy, w = p_control(Pc, Pr)

                wheel_speeds = wheel_velocity_transform(vx, vy, w)

                for i, pwm_forward, pwm_backward in zip(range(4), [pwm1, pwm2, pwm3, pwm4], [pwm5, pwm6, pwm7, pwm8]):
                    if wheel_speeds[i] > 0:
                        pwm_forward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] * speed))))
                        pwm_backward.ChangeDutyCycle(0)
                    else:
                        pwm_forward.ChangeDutyCycle(0)
                        pwm_backward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] * speed))))

            elif direction == 'square':
                if not square_path:
                    square_path = shapeGenerator('square', 1, 12)
                count = 0
                Pr = square_path[count]
                count += 1
                vx, vy, w = p_control(Pc, Pr)

                wheel_speeds = wheel_velocity_transform(vx, vy, w)

                for i, pwm_forward, pwm_backward in zip(range(4), [pwm1, pwm2, pwm3, pwm4], [pwm5, pwm6, pwm7, pwm8]):
                    if wheel_speeds[i] > 0:
                        pwm_forward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] * speed))))
                        pwm_backward.ChangeDutyCycle(0)
                    else:
                        pwm_forward.ChangeDutyCycle(0)
                        pwm_backward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] * speed))))

            elif direction == 'triangle':
                if not triangle_path:
                    triangle_path = shapeGenerator('triangle', 1, 12)
                count = 0
                Pr = triangle_path[count]
                count += 1
                vx, vy, w = p_control(Pc, Pr)

                wheel_speeds = wheel_velocity_transform(vx, vy, w)

                for i, pwm_forward, pwm_backward in zip(range(4), [pwm1, pwm2, pwm3, pwm4], [pwm5, pwm6, pwm7, pwm8]):
                    if wheel_speeds[i] > 0:
                        pwm_forward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] * speed))))
                        pwm_backward.ChangeDutyCycle(0)
                    else:
                        pwm_forward.ChangeDutyCycle(0)
                        pwm_backward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] * speed))))

            elif direction == 'hexagon':
                if not hexagon_path:
                    hexagon_path = shapeGenerator('hexagon', 1, 12)
                count = 0
                Pr = hexagon_path[count]
                count += 1
                vx, vy, w = p_control(Pc, Pr)

                wheel_speeds = wheel_velocity_transform(vx, vy, w)

                for i, pwm_forward, pwm_backward in zip(range(4), [pwm1, pwm2, pwm3, pwm4], [pwm5, pwm6, pwm7, pwm8]):
                    if wheel_speeds[i] > 0:
                        pwm_forward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] * speed))))
                        pwm_backward.ChangeDutyCycle(0)
                    else:
                        pwm_forward.ChangeDutyCycle(0)
                        pwm_backward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] * speed))))

        else:
            sleep(1)