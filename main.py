from time import sleep
import logging.config
from config import settings

from server import Server

def main():

    logging.config.fileConfig('log_config.ini') 

    logging.info("Starting the main program...")

    server = Server(host=settings.host_ip, port=settings.host_port)
    server.start()

    try:
        
        while True:
            # Simulate some work
            sleep(0.1)  # 100ms
            pass

    except KeyboardInterrupt:
        logging.error("Program terminated by user")

    except Exception as e:
        logging.error(f"Error in main loop: {e}")
    
    finally:
        logging.error("Cleaning up resources...")
        server.stop()
        

############################################

    # server_thread = robot_server.start()


    # # Initialize and start OptiTracker
    # print("Initializing OptiTracker...")
    # OptiTracker = 
    
    # # Initialize and start BeaconTracker in a separate thread
    # print("Initializing and starting BeaconTracker...")
    # BeaconTracker = BeaconLocalization(0, 0)
    # BeaconTracker.start_tracking()  # This starts its own thread
    
    # start_time = time()

    # # Define Robot Parameters
    # L1 = 0.06  # Distance between the center and the wheels (meters)
    # L2 = 0.07
    # R = 0.03  # Radius of the wheels (meters)
    # Kp = 1.5  # Proportional gain for velocity control
    # Kd = 1  # Derivative gain for velocity control

    # Pr = (1, 1)

    # wheel_positions = np.array([
    #     [L2, L1],   # Jobb első kerék
    #     [-L2, L1],  # Bal első kerék
    #     [-L2, -L1], # Bal hátsó kerék
    #     [L2, -L1],  # Jobb hátsó kerék
    # ])

    # def wheel_velocity_transform(vx, vy, w):
    #     wheel_velocities = np.array([
    #         #(1/R) * (vx + vy + (L1+L2) * w),  # Jobb hátsó kerék
    #         #(1/R) * (vx - vy + (L1+L2) * w),  # Jobb első kerék
    #         #(1/R) * (vx - vy - (L1+L2) * w),  # Bal hátsó kerék
    #         #(1/R) * (vx + vy - (L1+L2) * w),  # Bal első kerék

    #         #(1/R) * (-vx - vy - (L1+L2) * w),  # Jobb hátsó kerék
    #         #(1/R) * (-vx - vy - (L1+L2) * w),  # Jobb első kerék
    #         #(1/R) * (-vx - vy + (L1+L2) * w),  # Bal hátsó kerék
    #         #(1/R) * (-vx - vy + (L1+L2) * w),  # Bal első kerék

    #         (1/R) * (+vx + vy - (L1+L2) * w),  # Jobb hátsó kerék
    #         (1/R) * (-vx + vy - (L1+L2) * w),  # Jobb első kerék
    #         (1/R) * (-vx + vy + (L1+L2) * w),  # Bal hátsó kerék
    #         (1/R) * (+vx + vy + (L1+L2) * w),  # Bal első kerék

    #     ])
    #     print("vx:", vx)
    #     print("vy:", vy)
    #     return wheel_velocities

    # def p_control(current_pose, desired_pose, current_teta, desired_teta):
    #     error_x = desired_pose[0] - current_pose[0]
    #     error_y = desired_pose[1] - current_pose[1]
    #     error_theta = desired_teta - current_teta
        
    #     vx = Kp * error_x
    #     vy = Kp * error_y
    #     w = 0#Kd * error_theta
        
    #     print("error",error_x,error_y,error_theta)
    #     print("error szog",desired_teta,current_teta)
    #     #print("elvart",desired_pose[0])
    #     #print("jelenlegi",current_pose[0])

    #     return vx, vy, w

    # def automat_control(Pc, Pr, Tc, Tr):
    #     vx, vy, w = p_control(Pc, Pr, Tc, Tr)

    #     wheel_speeds = wheel_velocity_transform(vx, vy, w)

    #     for i, pwm_forward, pwm_backward in zip(range(4), [pwm[0], pwm[1], pwm[2], pwm[3]], [pwm[4], pwm[5], pwm[6], pwm[7]]):
    #         if wheel_speeds[i] > 0:
    #             duty = max(0, min(100, abs(wheel_speeds[i])))
    #             if duty < 20:
    #                 duty = 0
    #             pwm_forward.ChangeDutyCycle(duty)
    #             pwm_backward.ChangeDutyCycle(0)
    #         else:
    #             duty = max(0, min(100, abs(wheel_speeds[i])))
    #             if duty < 20:
    #                 duty = 0
    #             pwm_forward.ChangeDutyCycle(0)
    #             pwm_backward.ChangeDutyCycle(duty)

    # def shapeGenerator(shape, size, num_points):
    #     points = []
        
    #     if shape == 'circle':
    #         radius = math.sqrt(size)
    #         for _ in range(num_points):
    #             angle = random.uniform(0, 2 * math.pi)
    #             r = random.uniform(0, radius)
    #             x = r * math.cos(angle)
    #             y = r * math.sin(angle)
    #             points.append((x, y))
        
    #     elif shape == 'triangle':
    #         for _ in range(num_points):
    #             x = random.uniform(0, size)
    #             y = random.uniform(0, (size * math.sqrt(3)) / 2)
    #             if y > (math.sqrt(3) * x) or y > (-math.sqrt(3) * x + size * math.sqrt(3)):
    #                 continue
    #             points.append((x, y))
        
    #     elif shape == 'hexagon':
    #         for _ in range(num_points):
    #             angle = random.randint(0, 5) * math.pi / 3
    #             r = random.uniform(0, size)
    #             x = r * math.cos(angle)
    #             y = r * math.sin(angle)
    #             points.append((x, y))
        
    #     elif shape == 'square':
    #         for _ in range(num_points):
    #             x = random.uniform(-size / 2, size / 2)
    #             y = random.uniform(-size / 2, size / 2)
    #             points.append((x, y))
        
    #     return points

    # # This replaces the HTTP request with direct access to the server data
    # def direction_call():
    #     direction = robot_server.get_direction()
    #     speed = robot_server.get_speed()
    #     print("az irany:", direction)
    #     print("a sebesseg:", speed)
    #     return speed, direction

    # # Initialize path variables
    # circle_path = None
    # square_path = None
    # triangle_path = None
    # hexagon_path = None
    # count = 0

    # try:
    #     print("Main control loop starting...")
    #     while True:
    #         # delay 10ms
    #         sleep(0.1)  # 100ms
            
            
    #         OptiTracker.update_position()
    #         Po = OptiTracker.get_first_marker_coordinates()
    #         # BeaconTracker updates in its own thread, so we just need to get the coordinates
    #         Pb = BeaconTracker.get_coordinates()

    #         Po = (Po[0] if Po[0] is not None else 0.0, Po[1] if Po[1] is not None else 0.0)
    #         Pb = (Pb[0] if Pb[0] is not None else 0.0, Pb[1] if Pb[1] is not None else 0.0)

    #         print(f"DEBUG - Po: {Po}, Pb: {Pb}")
            
    #         # Update the server with the position data
    #         if Po[0] is not None and Po[1] is not None:
    #             robot_server.location = {"x": Po[0], "y": Po[1]}
            
    #         E = (Po[0] - Pb[0], Po[1] - Pb[1])

    #         elapsed_time = time() - start_time

    #         log_data = {
    #             'timestamp': f"{elapsed_time:.6f}",
    #             'Pr': Pr,
    #             'Po': Po,
    #             'Pb': Pb,
    #             'ERROR': E
    #         }
            
    #         with open('robot_log.json', 'a') as log_file:
    #             json.dump(log_data, log_file)
    #             log_file.write("\n")
            
    #         measure_mode = "Optitrack"
    #         manual_mode = False

    #         if measure_mode == 'Beacon':
    #             Pc = Pb
    #         else:
    #             Pc = Po

    #         Tc = OptiTracker.get_orientation_yaw()
    #         #print("Tc",Tc)
    #         Tr = math.atan2(Pr[1] - Pc[1], Pr[0] - Pc[0])

    #         #print("Tr",Tr)
    #         # Get direction and speed directly from the server instance
    #         speed, direction = direction_call()

    #         if direction:
    #             if manual_mode:
    #                 pwm = get_pwm_for_manual_control(direction, speed)
    #             else:
    #                 if direction == 'stop':
    #                     for i in range(8):
    #                         pwm[i].ChangeDutyCycle(0)
                            
    #                 elif direction == 'circle':
    #                     if not circle_path:
    #                         circle_path = shapeGenerator('circle', 1, 12)
    #                         count = 0
                        
    #                     Pr = (1,1) #circle_path[count]
    #                     count = (count + 1) % len(circle_path)
    #                     automat_control(Pc, Pr, Tc, Tr)
                        
    #                 elif direction == 'square':
    #                     if not square_path:
    #                         square_path = shapeGenerator('square', 1, 12)
    #                         count = 0

    #                     Pr = square_path[count]
    #                     count = (count + 1) % len(square_path)
    #                     automat_control(Pc, Pr, Tc, Tr)

    #                 elif direction == 'triangle':
    #                     if not triangle_path:
    #                         triangle_path = shapeGenerator('triangle', 1, 12)
    #                         count = 0

    #                     Pr = triangle_path[count]
    #                     count = (count + 1) % len(triangle_path)
    #                     automat_control(Pc, Pr, Tc, Tr)

    #                 elif direction == 'hexagon':
    #                     if not hexagon_path:
    #                         hexagon_path = shapeGenerator('hexagon', 1, 12)
    #                         count = 0

    #                     Pr = hexagon_path[count]
    #                     count = (count + 1) % len(hexagon_path)
    #                     automat_control(Pc, Pr, Tc, Tr)
    #         else:
    #             sleep(1)
                
    # except KeyboardInterrupt:
    #     print("Program terminated by user")
    # except Exception as e:
    #     print(f"Error in main loop: {e}")
    # finally:
    #     print("Cleaning up resources...")
    #     # Stop the BeaconTracker
    #     #BeaconTracker.stop_tracking()
        
    #     # Don't call pwm[i].stop() here anymore - that's handled by the atexit handler
    #     # Just set duty cycles to 0 as a precaution
    #     for i in range(8):
    #         try:
    #             pwm[i].ChangeDutyCycle(0)
    #         except:
    #             pass
        
    #     print("Resources cleaned up")

if __name__ == "__main__":
    main()