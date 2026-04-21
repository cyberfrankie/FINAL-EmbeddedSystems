# Control file for the RGB LED (common-cathode, 4-pin: R, GND, G, B)

import RPi.GPIO as GPIO


class RGBLed:

    def __init__(self, red_pin, green_pin, blue_pin):
        self._pins = {'r': red_pin, 'g': green_pin, 'b': blue_pin}
        for pin in self._pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def white(self):
        self._set(True, True, True)

    def red(self):
        self._set(True, False, False)

    def green(self):
        self._set(False, True, False)

    def off(self):
        self._set(False, False, False)

    def _set(self, r, g, b):
        GPIO.output(self._pins['r'], GPIO.HIGH if r else GPIO.LOW)
        GPIO.output(self._pins['g'], GPIO.HIGH if g else GPIO.LOW)
        GPIO.output(self._pins['b'], GPIO.HIGH if b else GPIO.LOW)

    def cleanup(self):
        self.off()
