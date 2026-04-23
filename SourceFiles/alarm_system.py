# controls the alarm system

import RPi.GPIO as GPIO


class AlarmSystem:

    MAX_ATTEMPTS = 3
    LED_FLASH_DURATION = 2.0

    def __init__(self, buzzer_pin=23, servo=None, led=None, ir_sensor=None):
        self._pin = buzzer_pin
        self._servo = servo
        self._led = led
        self._ir_sensor = ir_sensor
        self._unlocked = False   # persistent armed/disarmed state
        self._alarm_active = False
        self._failed_attempts = 0
        GPIO.setup(buzzer_pin, GPIO.OUT)
        GPIO.output(buzzer_pin, GPIO.LOW)

    def _flash_led(self, color):
        """Show `color` on the RGB LED and pause the IR sensor for LED_FLASH_DURATION."""
        if self._led:
            getattr(self._led, color)()
        if self._ir_sensor:
            self._ir_sensor.override(self.LED_FLASH_DURATION)

    def failed_attempt(self, lcd):
        self._failed_attempts += 1
        self._flash_led('red')
        print(f"Failed attempt {self._failed_attempts}/{self.MAX_ATTEMPTS}")
        if self._failed_attempts >= self.MAX_ATTEMPTS:
            self._failed_attempts = 0
            self._alarm_active = True
            GPIO.output(self._pin, GPIO.HIGH)
            lcd.show_alarm()
            print("Too many failed attempts - triggering alarm!")
        else:
            lcd.show_denied()

    def disarm(self, lcd):
        self._failed_attempts = 0
        if self._alarm_active:
            self._alarm_active = False
            GPIO.output(self._pin, GPIO.LOW)
        self._unlocked = True
        self._flash_led('green')
        if self._servo:
            self._servo.unlock()
        lcd.show_unlocked()
        print("System disarmed/unlocked.")

    def rearm(self, lcd):
        self._unlocked = False
        if self._servo:
            self._servo.lock()
        lcd.show_armed()
        print("System re-armed.")

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
