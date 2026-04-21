# controls the alarm system

import RPi.GPIO as GPIO


class AlarmSystem:

    MAX_ATTEMPTS = 3

    def __init__(self, buzzer_pin=23, servo=None):
        self._pin = buzzer_pin
        self._servo = servo
        self._unlocked = False   # persistent armed/disarmed state
        self._alarm_active = False
        self._failed_attempts = 0
        GPIO.setup(buzzer_pin, GPIO.OUT)
        GPIO.output(buzzer_pin, GPIO.LOW)

    def failed_attempt(self, lcd):
        self._failed_attempts += 1
        print(f"Failed attempt {self._failed_attempts}/{self.MAX_ATTEMPTS}")
        if self._failed_attempts >= self.MAX_ATTEMPTS:
            self._failed_attempts = 0
            self._alarm_active = True
            GPIO.output(self._pin, GPIO.HIGH)
            lcd.show_alarm()
            print("Too many failed attempts - triggering alarm!")
        else:
            lcd.show_denied()

    def toggle_unlock(self, lcd):
        self._failed_attempts = 0
        if self._alarm_active:
            self._alarm_active = False
            GPIO.output(self._pin, GPIO.LOW)
        if self._unlocked:
            self._unlocked = False
            if self._servo:
                self._servo.lock()
            lcd.show_armed()
            print("System re-armed.")
        else:
            self._unlocked = True
            if self._servo:
                self._servo.unlock()
            lcd.show_unlocked()
            print("System disarmed/unlocked.")

    def door_pressed(self, lcd):
        if self._alarm_active:
            self._alarm_active = False
            self._failed_attempts = 0
            GPIO.output(self._pin, GPIO.LOW)
            lcd.reset()
            print("Alarm silenced.")
        elif self._unlocked:
            print("Door opened - system is unlocked.")
        else:
            print("Unauthorized door attempt - triggering alarm!")
            self._alarm_active = True
            GPIO.output(self._pin, GPIO.HIGH)
            lcd.show_alarm()

    def cleanup(self):
        self._alarm_active = False
        GPIO.output(self._pin, GPIO.LOW)
