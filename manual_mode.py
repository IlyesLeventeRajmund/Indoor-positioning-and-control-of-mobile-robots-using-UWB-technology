def Manual_Controling(pwm,direction,speed):
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