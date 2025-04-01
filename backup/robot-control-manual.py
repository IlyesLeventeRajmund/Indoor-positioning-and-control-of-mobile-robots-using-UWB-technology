import RPi.GPIO as GPIO
from time import sleep
import requests

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
        direction_response = requests.get('http://10.42.0.1:5001/current_direction')
        speed_response = requests.get('http://10.42.0.1:5001/current_speed')
        print("a valasz:",direction_response.json().get("direction"))
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
            elif direction == 'circle' :
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
            elif direction == 'square' :
                fordulas=35*(1/speed)
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
                sleep(1)
                #fordul
                #hatra
                pwm1.ChangeDutyCycle(speed)   #jh
                pwm2.ChangeDutyCycle(speed)   #je
                pwm3.ChangeDutyCycle(0)   #bh
                pwm4.ChangeDutyCycle(0)   #be

                #elore
                pwm5.ChangeDutyCycle(0)  #jh
                pwm6.ChangeDutyCycle(0)  #je
                pwm7.ChangeDutyCycle(speed)  #bh
                pwm8.ChangeDutyCycle(speed)  #be
                sleep(fordulas)

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
                sleep(1)
                #fordul
                #hatra
                pwm1.ChangeDutyCycle(speed)   #jh
                pwm2.ChangeDutyCycle(speed)   #je
                pwm3.ChangeDutyCycle(0)   #bh
                pwm4.ChangeDutyCycle(0)   #be

                #elore
                pwm5.ChangeDutyCycle(0)  #jh
                pwm6.ChangeDutyCycle(0)  #je
                pwm7.ChangeDutyCycle(speed)  #bh
                pwm8.ChangeDutyCycle(speed)  #be
                sleep(fordulas)

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
                sleep(1)
                #fordul
                #hatra
                pwm1.ChangeDutyCycle(speed)   #jh
                pwm2.ChangeDutyCycle(speed)   #je
                pwm3.ChangeDutyCycle(0)   #bh
                pwm4.ChangeDutyCycle(0)   #be

                #elore
                pwm5.ChangeDutyCycle(0)  #jh
                pwm6.ChangeDutyCycle(0)  #je
                pwm7.ChangeDutyCycle(speed)  #bh
                pwm8.ChangeDutyCycle(speed)  #be
                sleep(fordulas)

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
                sleep(1)
                #fordul
                #hatra
                pwm1.ChangeDutyCycle(speed)   #jh
                pwm2.ChangeDutyCycle(speed)   #je
                pwm3.ChangeDutyCycle(0)   #bh
                pwm4.ChangeDutyCycle(0)   #be

                #elore
                pwm5.ChangeDutyCycle(0)  #jh
                pwm6.ChangeDutyCycle(0)  #je
                pwm7.ChangeDutyCycle(speed)  #bh
                pwm8.ChangeDutyCycle(speed)  #be
                sleep(fordulas)
            elif direction == 'triangle' :
                pwm5.ChangeDutyCycle(0) 
            elif direction == 'hexagon' :
                pwm5.ChangeDutyCycle(0) 
        else:
            sleep(1)