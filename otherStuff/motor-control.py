import RPi.GPIO as GPIO
from time import sleep
import requests

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

pwm1 = GPIO.PWM(2, 1000)  
pwm2 = GPIO.PWM(5, 1000) 
pwm3 = GPIO.PWM(10, 1000)
pwm4 = GPIO.PWM(22, 1000)

pwm5 = GPIO.PWM(3, 1000) 
pwm6 = GPIO.PWM(6, 1000)  
pwm7 = GPIO.PWM(9, 1000) 
pwm8 = GPIO.PWM(11, 1000)  

pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)

pwm5.start(0)
pwm6.start(0)
pwm7.start(0)
pwm8.start(0)


while True:
        direction = 'up'
        if direction == 'up':
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(25)
            pwm3.ChangeDutyCycle(0)
            pwm4.ChangeDutyCycle(25)

            pwm5.ChangeDutyCycle(0)
            pwm6.ChangeDutyCycle(0)
            pwm7.ChangeDutyCycle(0)
            pwm8.ChangeDutyCycle(0)

#------------------------------------------------------------------------------------------------------------
#import RPi.GPIO as GPIO
#from time import sleep

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(2, GPIO.OUT)
#GPIO.setup(3, GPIO.OUT)
#GPIO.setup(4, GPIO.OUT)

#GPIO.output(2, True)
#GPIO.output(3, False)

#pwm = GPIO.PWM(4, 1000) 
#pwm.start(0)
#while True:
#    for duty in range(0, 101, 1):
 #       pwm.ChangeDutyCycle(100)
 #       sleep(0.01)
 #   sleep(0.5)
#---------------------------------------------------------------------------------------------------------------
#pololu 2135    
# for _ in range(5):
#     GPIO.output(2, True)
#     GPIO.output(3, False)
#     print("elore")
#     sleep(0.5)
#     GPIO.output(2, False)
#     GPIO.output(3, False)
#     print("megall")
#     sleep(0.5)
#     GPIO.output(2, False)
#     GPIO.output(3, True)
#     print("hatra")
#     sleep(0.5)
#     GPIO.output(2, False)
#     GPIO.output(3, False)
#     print("megall")
#     sleep(0.5)
    

# pwm = GPIO.PWM(18, 1000)  # 1000 Hz frequency
# pwm.start(0)  # Initial duty cycle 0%

# while True:
#     for duty in range(0, 101, 1):
#         pwm.ChangeDutyCycle(duty)
#         sleep(0.01)
#     sleep(0.5)
#     for duty in range(100, -1, -1):
#         pwm.ChangeDutyCycle(duty)
#         sleep(0.01)
#     sleep(0.5)