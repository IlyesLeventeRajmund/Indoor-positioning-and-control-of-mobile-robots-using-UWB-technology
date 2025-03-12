import RPi.GPIO as GPIO
import time
import requests

# Pin konfiguráció
TRIG = 13
ECHO = 19

# GPIO inicializálás
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        # Trig jel küldése
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

        print(f"Távolság: {distance} cm")

except KeyboardInterrupt:
    GPIO.cleanup()
