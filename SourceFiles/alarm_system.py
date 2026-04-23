# controls the alarm system

import time
import threading
import RPi.GPIO as GPIO


class AlarmSystem:

    MAX_ATTEMPTS = 3
    LED_FLASH_DURATION = 2.0

    def __init__(self, buzzer_pin=23, servo=None, led=None):
        self._pin = buzzer_pin
        self._servo = servo
        self._led = led
        self._unlocked = False   # persistent armed/disarmed state
        self._alarm_active = False
        self._failed_attempts = 0
        GPIO.setup(buzzer_pin, GPIO.OUT)
        GPIO.output(buzzer_pin, GPIO.LOW)

    def _flash_led(self, color):
        """Flash `color` on the RGB LED for LED_FLASH_DURATION seconds, then turn it off."""
        if self._led:
            getattr(self._led, color)()
            t = threading.Timer(self.LED_FLASH_DURATION, self._led.off)
            t.daemon = True
            t.start()

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

    def doorbell(self):
        def _beep():
            for _ in range(3):
                GPIO.output(self._pin, GPIO.HIGH)
                time.sleep(0.15)
                GPIO.output(self._pin, GPIO.LOW)
                time.sleep(0.15)
        threading.Thread(target=_beep, daemon=True).start()

    def cleanup(self):
        self._alarm_active = False
        GPIO.output(self._pin, GPIO.LOW)
