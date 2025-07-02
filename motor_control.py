# motor_control.py

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

ENA = 17
IN1 = 27
IN2 = 22
ENB = 18
IN3 = 23
IN4 = 24

GPIO.setup([ENA, IN1, IN2, ENB, IN3, IN4], GPIO.OUT)

pwm_left = GPIO.PWM(ENA, 100)  # Frecuencia 100Hz
pwm_right = GPIO.PWM(ENB, 100)

pwm_left.start(0)
pwm_right.start(0)

def stop():
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)

def move(left_speed, right_speed):
    def set_motor(speed, in1, in2):
        if speed > 0:
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
        elif speed < 0:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
        else:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)

    set_motor(left_speed, IN1, IN2)
    set_motor(right_speed, IN3, IN4)

    pwm_left.ChangeDutyCycle(abs(left_speed) if left_speed != 0 else 0)
    pwm_right.ChangeDutyCycle(abs(right_speed) if right_speed != 0 else 0)