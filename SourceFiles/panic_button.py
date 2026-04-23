# Panic Button control file

import RPi.GPIO as GPIO


class PanicButton:

    def __init__(self, pin, alarm, lcd):
        self._pin = pin
        self._alarm = alarm
        self._lcd = lcd
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self._handle, bouncetime=300)

    def _handle(self, channel):
        if self._alarm._panic_active:
            self._alarm.stop_panic(self._lcd)
        else:
            self._alarm.panic(self._lcd)

    def cleanup(self):
        GPIO.remove_event_detect(self._pin)
