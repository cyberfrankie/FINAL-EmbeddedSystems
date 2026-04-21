# Python script detecting the push button

import RPi.GPIO as GPIO


class PushButton:

    def __init__(self, pin=18, on_press=None):
        self._pin = pin
        self._on_press = on_press
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self._handle, bouncetime=300)

    def _handle(self, channel):
        if self._on_press:
            self._on_press()

    def cleanup(self):
        GPIO.remove_event_detect(self._pin)
