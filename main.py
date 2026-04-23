# Main Python Script

import sys
import os
import RPi.GPIO as GPIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'SourceFiles'))

from lcd_display import LCDDisplay
from alarm_system import AlarmSystem
from push_button import PushButton
from keypad_receiver import KeypadReceiver
from servo_lock import ServoLock
from led_control import RGBLed, WhiteLed
from infrared_sensor import InfraredSensor

# GPIO mode set once here so all modules share the same context
GPIO.setmode(GPIO.BCM)

# Hardware config — update pins/port to match your wiring
SERIAL_PORT  = '/dev/ttyACM0'   # or /dev/ttyUSB0
LCD_ADDRESS  = 0x27             # run 'sudo i2cdetect -y 1' to confirm (may be 0x3F)
BUZZER_PIN   = 23               # BCM pin for buzzer
BUTTON_PIN   = 18               # BCM pin for push button (doorknob)
SERVO_PIN    = 17               # BCM pin for servo signal wire

# RGB LED pins (common-anode: longest pin to 3.3V)
LED_RED_PIN   = 13
LED_GREEN_PIN = 19
LED_BLUE_PIN  = 26

# White LED pin (motion sensor indicator)
WHITE_LED_PIN = 6

# HW-416 IR sensor digital output pin
IR_PIN = 16

rgb_led   = RGBLed(red_pin=LED_RED_PIN, green_pin=LED_GREEN_PIN, blue_pin=LED_BLUE_PIN)
white_led = WhiteLed(pin=WHITE_LED_PIN)
ir        = InfraredSensor(signal_pin=IR_PIN, led=white_led)
lcd       = LCDDisplay(i2c_address=LCD_ADDRESS)
servo     = ServoLock(pin=SERVO_PIN)
alarm     = AlarmSystem(buzzer_pin=BUZZER_PIN, servo=servo, led=rgb_led)
button    = PushButton(pin=BUTTON_PIN, on_press=lambda: alarm.door_pressed(lcd))
receiver  = KeypadReceiver(port=SERIAL_PORT, lcd=lcd, alarm=alarm)

ir.start()

try:
    receiver.run()
except KeyboardInterrupt:
    print("\nShutting down.")
finally:
    ir.cleanup()
    alarm.cleanup()
    button.cleanup()
    servo.cleanup()
    rgb_led.cleanup()
    white_led.cleanup()
    GPIO.cleanup()
