# Main Python Script

import sys
import os
import RPi.GPIO as GPIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Part1_Doorlock_Alarm'))

from lcd_display import LCDDisplay
from alarm_system import AlarmSystem
from push_button import PushButton
from keypad_receiver import KeypadReceiver
from servo_lock import ServoLock

# GPIO mode set once here so all modules share the same context
GPIO.setmode(GPIO.BCM)

# Hardware config — update pins/port to match your wiring
SERIAL_PORT  = '/dev/ttyACM0'   # or /dev/ttyACM0
LCD_ADDRESS  = 0x27             # run 'sudo i2cdetect -y 1' to confirm (may be 0x3F)
BUZZER_PIN   = 23               # BCM pin for buzzer
BUTTON_PIN   = 18               # BCM pin for push button (doorknob)
SERVO_PIN    = 17               # BCM pin for servo signal wire

lcd      = LCDDisplay(i2c_address=LCD_ADDRESS)
servo    = ServoLock(pin=SERVO_PIN)
alarm    = AlarmSystem(buzzer_pin=BUZZER_PIN, servo=servo)
button   = PushButton(pin=BUTTON_PIN, on_press=lambda: alarm.door_pressed(lcd))
receiver = KeypadReceiver(port=SERIAL_PORT, lcd=lcd, alarm=alarm)

try:
    receiver.run()
except KeyboardInterrupt:
    print("\nShutting down.")
finally:
    alarm.cleanup()
    button.cleanup()
    servo.cleanup()
    GPIO.cleanup()
