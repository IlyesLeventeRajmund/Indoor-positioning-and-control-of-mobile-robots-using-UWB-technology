import RPi.GPIO as GPIO
from time import sleep
import requests

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)


pwm1 = GPIO.PWM(2, 1000)  
pwm2 = GPIO.PWM(3, 1000) 
pwm3 = GPIO.PWM(5, 1000) 
pwm4 = GPIO.PWM(6, 1000)  


pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)

      
while True:
        direction_response = requests.get('http://10.42.0.1:5001/current_direction')
        speed_response = requests.get('http://10.42.0.1:5001/current_speed')
        print("a valasz:",direction_response.json().get("direction"))
        print("a sebesseg:",speed_response.json().get("speed"))
        if direction_response.ok:
            direction = direction_response.json().get("direction")
            speed = speed_response.json().get("speed")
            if direction == 'up':
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(speed)
                pwm4.ChangeDutyCycle(0)
            elif direction == 'down':
                pwm1.ChangeDutyCycle(speed)
                pwm2.ChangeDutyCycle(0)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(speed)
            elif direction == 'left':
                pwm1.ChangeDutyCycle(0)
            elif direction == 'right':
                pwm1.ChangeDutyCycle(0)
            elif direction == 'stop' :
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(0)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(0)
            if direction == 'up-left':
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(20)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(20)
            elif direction == 'up-right':
                pwm1.ChangeDutyCycle(20)   #jh
                pwm2.ChangeDutyCycle(0)   #je
                pwm3.ChangeDutyCycle(20)   #bh
                pwm4.ChangeDutyCycle(0)   #be
            elif direction == 'down-left':
                pwm1.ChangeDutyCycle(0)
            elif direction == 'down-right':
                pwm1.ChangeDutyCycle(0)  #be
            elif direction == 'circle' :
                #hatra
                pwm1.ChangeDutyCycle(0)   #jh
            elif direction == 'square' :
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(speed)
                pwm4.ChangeDutyCycle(0)
                sleep(2)
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(speed)
                sleep(0.75)

                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(speed)
                pwm4.ChangeDutyCycle(0)
                sleep(2)
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(speed)
                sleep(0.75)

                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(speed)
                pwm4.ChangeDutyCycle(0)
                sleep(2)
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(speed)
                sleep(0.75)

                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(speed)
                pwm4.ChangeDutyCycle(0)
                sleep(2)
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(speed)
                sleep(0.75)
            elif direction == 'triangle' :
                pwm1.ChangeDutyCycle(0) 
            elif direction == 'hexagon' :
                pwm1.ChangeDutyCycle(0) 
        else:
            sleep(1)