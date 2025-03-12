import RPi.GPIO as GPIO
import time
from time import sleep
import requests

# Pin konfiguráció
TRIG = 13
ECHO = 19

# GPIO inicializálás
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

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
    print("a valasz:", direction_response.json().get("direction"))
    print("a sebesseg:", speed_response.json().get("speed"))

    GPIO.output(TRIG, False)
    time.sleep(0.1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Várakozás az Echo jel fogadására
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Távolság számítása
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    # Távolság küldése a szerverre
    distance_data = {"distance": distance}
    distance_response = requests.post('http://10.42.0.1:5001/distance', json=distance_data)
    distance_response.raise_for_status()
    #print("a tavolsag:", distance_response.json().get("distance"))

    speed = speed_response.json().get("speed")
    if distance > 40 :
        if direction_response.ok:
            direction = direction_response.json().get("direction")
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
                pwm2.ChangeDutyCycle(speed)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(speed)
            elif direction == 'right':
                pwm1.ChangeDutyCycle(speed)
                pwm2.ChangeDutyCycle(0)
                pwm3.ChangeDutyCycle(speed)
                pwm4.ChangeDutyCycle(0)
            elif direction == 'stop' :
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(0)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(0)
    else:
        #fordul
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(speed)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(speed)
        sleep(0.25)
