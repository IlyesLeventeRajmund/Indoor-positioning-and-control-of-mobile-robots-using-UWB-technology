import atexit
from time import time
import platform

# Check if the platform is Raspberry Pi
if platform.machine().startswith('arm'):
    print("Running on Pi — GPIO Enabled.")
    
else:
    print("Running off Pi — Mocking GPIO.")
    import sys
    from unittest import mock

    # Mock the entire RPi.GPIO module
    # Create a mock GPIO module
    mock_gpio = mock.MagicMock()
    mock_gpio.BCM = 'BCM'
    mock_gpio.OUT = 'OUT'
    mock_gpio.IN = 'IN'
    mock_gpio.HIGH = 1
    mock_gpio.LOW = 0

    sys.modules['RPi'] = mock.MagicMock()
    sys.modules['RPi.GPIO'] = mock_gpio

    # mock_gpio.setmode.side_effect = lambda mode: print(f"[MOCK] GPIO.setmode({mode})")
    # mock_gpio.setup.side_effect = lambda pin, mode: print(f"[MOCK] GPIO.setup({pin}, {mode})")
    # mock_gpio.output.side_effect = lambda pin, value: print(f"[MOCK] GPIO.output({pin}, {value})")
    # mock_gpio.cleanup.side_effect = lambda: print("[MOCK] GPIO.cleanup()")

import RPi.GPIO as GPIO

def initialize_gpio():
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

def set_pwm_for_manual_control(pwm, direction, speed):
    if direction == 'up':
        #hatra
        pwm[0].ChangeDutyCycle(0)   #jh
        pwm[1].ChangeDutyCycle(0)   #je
        pwm[2].ChangeDutyCycle(0)   #bh
        pwm[3].ChangeDutyCycle(0)   #be

        #elore
        pwm[4].ChangeDutyCycle(speed)  #jh
        pwm[5].ChangeDutyCycle(speed)  #je
        pwm[6].ChangeDutyCycle(speed)  #bh
        pwm[7].ChangeDutyCycle(speed)  #be
    elif direction == 'down':
        pwm[0].ChangeDutyCycle(speed)
        pwm[1].ChangeDutyCycle(speed)
        pwm[2].ChangeDutyCycle(speed)
        pwm[3].ChangeDutyCycle(speed)

        pwm[4].ChangeDutyCycle(0)
        pwm[5].ChangeDutyCycle(0)
        pwm[6].ChangeDutyCycle(0)
        pwm[7].ChangeDutyCycle(0)
    elif direction == 'left':
        pwm[0].ChangeDutyCycle(0)
        pwm[1].ChangeDutyCycle(speed)
        pwm[2].ChangeDutyCycle(speed)
        pwm[3].ChangeDutyCycle(0)

        pwm[4].ChangeDutyCycle(speed)
        pwm[5].ChangeDutyCycle(0)
        pwm[6].ChangeDutyCycle(0)
        pwm[7].ChangeDutyCycle(speed)
    elif direction == 'right':
        pwm[0].ChangeDutyCycle(speed)
        pwm[1].ChangeDutyCycle(0)
        pwm[2].ChangeDutyCycle(0)
        pwm[3].ChangeDutyCycle(speed)

        pwm[4].ChangeDutyCycle(0)
        pwm[5].ChangeDutyCycle(speed)
        pwm[6].ChangeDutyCycle(speed)
        pwm[7].ChangeDutyCycle(0)
    elif direction == 'stop' :
        pwm[0].ChangeDutyCycle(0)
        pwm[1].ChangeDutyCycle(0)
        pwm[2].ChangeDutyCycle(0)
        pwm[3].ChangeDutyCycle(0)

        pwm[4].ChangeDutyCycle(0)
        pwm[5].ChangeDutyCycle(0)
        pwm[6].ChangeDutyCycle(0)
        pwm[7].ChangeDutyCycle(0)
    elif direction == 'up-left':
        #hatra
        pwm[0].ChangeDutyCycle(0)   #jh
        pwm[1].ChangeDutyCycle(0)   #je
        pwm[2].ChangeDutyCycle(0)   #bh
        pwm[3].ChangeDutyCycle(0)   #be

        #elore
        pwm[4].ChangeDutyCycle(speed)  #jh
        pwm[5].ChangeDutyCycle(0)  #je
        pwm[6].ChangeDutyCycle(0)  #bh
        pwm[7].ChangeDutyCycle(speed)  #be
    elif direction == 'up-right':
        #hatra
        pwm[0].ChangeDutyCycle(0)   #jh
        pwm[1].ChangeDutyCycle(0)   #je
        pwm[2].ChangeDutyCycle(0)   #bh
        pwm[3].ChangeDutyCycle(0)   #be

        #elore
        pwm[4].ChangeDutyCycle(0)  #jh
        pwm[5].ChangeDutyCycle(speed)  #je
        pwm[6].ChangeDutyCycle(speed)  #bh
        pwm[7].ChangeDutyCycle(0)  #be
    elif direction == 'down-left':
        #hatra
        pwm[0].ChangeDutyCycle(0)   #jh
        pwm[1].ChangeDutyCycle(speed)   #je
        pwm[2].ChangeDutyCycle(speed)   #bh
        pwm[3].ChangeDutyCycle(0)   #be

        #elore
        pwm[4].ChangeDutyCycle(0)  #jh
        pwm[5].ChangeDutyCycle(0)  #je
        pwm[6].ChangeDutyCycle(0)  #bh
        pwm[7].ChangeDutyCycle(0)  #be
    elif direction == 'down-right':
        #hatra
        pwm[0].ChangeDutyCycle(speed)   #jh
        pwm[1].ChangeDutyCycle(0)   #je
        pwm[2].ChangeDutyCycle(0)   #bh
        pwm[3].ChangeDutyCycle(speed)   #be

        #elore
        pwm[4].ChangeDutyCycle(0)  #jh
        pwm[5].ChangeDutyCycle(0)  #je
        pwm[6].ChangeDutyCycle(0)  #bh
        pwm[7].ChangeDutyCycle(0)  #be
