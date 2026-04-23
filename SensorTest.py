import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

print("Reading IR sensor on GPIO 16 - move hand in/out of range (Ctrl+C to stop)")
try:
    while True:
        val = GPIO.input(16)
        print(f"GPIO 16 = {val}  ({'DETECTED' if val == 0 else 'CLEAR'})", end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()