# Control file for the RGB LED (common-anode, 4-pin: R, VCC, G, B)
# Common anode: longest pin to 3.3V. LOW = on, HIGH = off.

import RPi.GPIO as GPIO


class RGBLed:

    def __init__(self, red_pin, green_pin, blue_pin):
        self._pins = {'r': red_pin, 'g': green_pin, 'b': blue_pin}
        for pin in self._pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)  # HIGH = off for common anode

    def white(self):
        self._set(True, True, True)

    def red(self):
        self._set(True, False, False)

    def green(self):
        self._set(False, True, False)

    def off(self):
        self._set(False, False, False)

    def _set(self, r, g, b):
        GPIO.output(self._pins['r'], GPIO.LOW if r else GPIO.HIGH)
        GPIO.output(self._pins['g'], GPIO.LOW if g else GPIO.HIGH)
        GPIO.output(self._pins['b'], GPIO.LOW if b else GPIO.HIGH)

    def cleanup(self):
        self.off()


class WhiteLed:

    def __init__(self, pin):
        self._pin = pin
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def on(self):
        GPIO.output(self._pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self._pin, GPIO.LOW)

    def cleanup(self):
        self.off()
