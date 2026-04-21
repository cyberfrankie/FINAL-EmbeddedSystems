import RPi.GPIO as GPIO
import time


class ServoLock:

    LOCKED_ANGLE   = 0    # degrees
    UNLOCKED_ANGLE = 90   # degrees

    def __init__(self, pin=17):
        self._pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self._pwm = GPIO.PWM(pin, 50)  # 50 Hz for standard servo
        self._pwm.start(0)
        self._set_angle(self.LOCKED_ANGLE)

    def unlock(self):
        self._set_angle(self.UNLOCKED_ANGLE)
        print("Servo: door unlocked.")

    def lock(self):
        self._set_angle(self.LOCKED_ANGLE)
        print("Servo: door locked.")

    def _set_angle(self, angle):
        # Maps 0-180° → 2.5-12.5% duty cycle (standard servo pulse range)
        duty = angle / 18.0 + 2.5
        self._pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        self._pwm.ChangeDutyCycle(0)  # stop pulses to prevent jitter

    def cleanup(self):
        self._pwm.stop()
