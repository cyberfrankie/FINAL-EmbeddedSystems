# Receives input from Arduino to us on Pi

import serial


class KeypadReceiver:

    def __init__(self, port, lcd, alarm, baud=9600):
        self._ser = serial.Serial(port, baud, timeout=1)
        self._lcd = lcd
        self._alarm = alarm

    def run(self):
        print("Listening for keypad input...")
        while True:
            line = self._ser.readline().decode('utf-8').strip()
            if line:
                print(f"Received: {line}")
                if line == "KEY":
                    self._lcd.key_pressed()
                elif line == "CORRECT":
                    print("Correct code - toggling lock state.")
                    self._alarm.toggle_unlock(self._lcd)
                elif line == "INCORRECT":
                    print("Access denied!")
                    self._alarm.failed_attempt(self._lcd)
                elif line == "CLEARED":
                    print("Input cleared.")
                    self._lcd.clear_input()
