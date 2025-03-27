import RPi.GPIO as GPIO
from time import time
from time import sleep
from datetime import datetime
import requests
import numpy as np
import json
import OptitrackData
import RobotLocationData
import ManualModeData
import random
import math
import httpx

def gpioInit():
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

    return pwm1, pwm2, pwm3, pwm4, pwm5, pwm6, pwm7, pwm8

pwm= gpioInit()

OptiTracker = OptitrackData.RobotLocationOptitrack()
BeaconTracker = RobotLocationData.RobotLocationBeacon(0,0)

start_time = time()

# Define Robot Parameters
L1 = 0.06  # Distance between the center and the wheels (meters)
L2 = 0.07
R = 0.03  # Radius of the wheels (meters)
Kp = 2  # Proportional gain for velocity control
Kd = 0.1  # Derivative gain for velocity control

wheel_positions = np.array([
    [ L2,  L1],  # Jobb első kerék
    [-L2,  L1],  # Bal első kerék
    [-L2, -L1],  # Bal hátsó kerék
    [ L2, -L1],  # Jobb hátsó kerék
])

def wheel_velocity_transform(vx, vy, w):
    wheel_velocities = np.array([
        (1/R) * (vx + vy + L1 * w),  # Jobb hátsó kerék
        (1/R) * (vx + vy - L2 * w),  # Jobb első kerék
        (1/R) * (vx - vy - L1 * w),  # Bal hátsó kerék
        (1/R) * (vx - vy + L2 * w),  # Bal első kerék
    ])
    print("vx:",vx)
    print("vy:",vy)
    return wheel_velocities

def p_control(current_pose, desired_pose):
    error_x = desired_pose[0] - current_pose[0]
    error_y = desired_pose[1] - current_pose[1]
    error_theta = 0 #desired_pose[2] - current_pose[2]
    
    vx = Kp * error_x
    vy = Kp * error_y
    w = Kd * error_theta
    
    return vx, vy, w

def automat_control(Pc,Pr):
    vx, vy, w = p_control(Pc, Pr)

    wheel_speeds = wheel_velocity_transform(vx, vy, w)

    for i, pwm_forward, pwm_backward in zip(range(4), [pwm[0], pwm[1], pwm[2], pwm[3]], [pwm[4], pwm[5], pwm[6], pwm[7]]):
        if wheel_speeds[i] > 0:
            pwm_forward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] ))))
            pwm_backward.ChangeDutyCycle(0)
        else:
            pwm_forward.ChangeDutyCycle(0)
            pwm_backward.ChangeDutyCycle(max(0, min(100, abs(wheel_speeds[i] ))))


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

def direction_call():
    direction_response = requests.get('http://10.42.0.1:5001/current_direction')
    speed_response = requests.get('http://10.42.0.1:5001/current_speed')
    print("az irany:",direction_response.json().get("direction"))
    print("a sebesseg:",speed_response.json().get("speed"))
    direction = direction_response.json().get("direction")
    speed = speed_response.json().get("speed")
    return speed, direction

async def direction_call_fastapi():
    async with httpx.AsyncClient() as client:
        direction_response = await client.get('http://10.42.0.1:5001/current_direction')
        speed_response = await client.get('http://10.42.0.1:5001/current_speed')
    
    direction = direction_response.json().get("direction")
    speed = speed_response.json().get("speed")
    return speed, direction
 
while True:
    #delay 10ms
    sleep(0.1) #100ms
    #megmerni a teljes ciklus idot

    Pr = (0,0)
    OptiTracker.update_position()
    #OptiTracker.update_position_fastapi()
    Po = OptiTracker.get_first_marker_coordinates()
    BeaconTracker.update_position()
    #BeaconTracker.update_position_fastapi()
    Pb = BeaconTracker.get_coordinates()

    Po = (Po[0] if Po[0] is not None else 0.0, Po[1] if Po[1] is not None else 0.0)
    Pb = (Pb[0] if Pb[0] is not None else 0.0, Pb[1] if Pb[1] is not None else 0.0)

    print(f"DEBUG - Po: {Po}, Pb: {Pb}")
    
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

    if measure_mode =='Beacon':
        Pc = Pb
    else:
        Pc = Po
    
    speed, direction =direction_call()
    #speed, direction =direction_call_fastapi()

    if direction:
        if manual_mode:
            ManualModeData.Manual_Controling(pwm,direction,speed)
        else:
            if direction == 'stop' :
                pwm[0].ChangeDutyCycle(0)   #jh
                pwm[1].ChangeDutyCycle(0)   #je
                pwm[2].ChangeDutyCycle(0)   #bh
                pwm[3].ChangeDutyCycle(0)   #be

                pwm[0].ChangeDutyCycle(0)   #jh
                pwm[1].ChangeDutyCycle(0)   #je
                pwm[2].ChangeDutyCycle(0)   #bh
                pwm[3].ChangeDutyCycle(0)   #be
            elif direction == 'circle':
                '''if not circle_path:
                    circle_path = shapeGenerator('circle', 1, 12)
                    count = 0
                
                Pr = circle_path[count]
                count += 1'''

                Pr = (0,0)
                automat_control(Pc, Pr)
                
            elif direction == 'square':
                if not square_path:
                    square_path = shapeGenerator('square', 1, 12)
                    count = 0

                Pr = square_path[count]
                count += 1

                automat_control(Pc, Pr)

            elif direction == 'triangle':
                if not triangle_path:
                    triangle_path = shapeGenerator('triangle', 1, 12)
                    count = 0

                Pr = triangle_path[count]
                count += 1

                automat_control(Pc, Pr)


            elif direction == 'hexagon':
                if not hexagon_path:
                    hexagon_path = shapeGenerator('hexagon', 1, 12)
                    count = 0

                Pr = hexagon_path[count]
                count += 1
                automat_control(Pc, Pr)
                
            
    else:
        sleep(1)