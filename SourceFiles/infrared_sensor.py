# Setup file for the HW-416 IR sensor
# The HW-416 outputs LOW when an object is within the potentiometer-set range.
# Set the onboard pot so the threshold distance is ~30 cm.

import RPi.GPIO as GPIO
import threading
import time


class InfraredSensor:

    def __init__(self, signal_pin, led, poll_interval=0.1):
        self._pin = signal_pin
        self._led = led
        self._poll_interval = poll_interval
        self._running = False
        self._motion_active = False
        self._thread = None
        GPIO.setup(signal_pin, GPIO.IN)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            detected = GPIO.input(self._pin) == GPIO.HIGH

            if detected and not self._motion_active:
                self._motion_active = True
                self._led.on()
            elif not detected and self._motion_active:
                self._motion_active = False
                self._led.off()

            time.sleep(self._poll_interval)

    def cleanup(self):
        self.stop()
