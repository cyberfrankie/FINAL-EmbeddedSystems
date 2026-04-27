# Controls the LCD display for each stage

from RPLCD.i2c import CharLCD
import threading


class LCDDisplay:

    def __init__(self, i2c_address=0x27):
        self.lcd = CharLCD(
            i2c_expander='PCF8574',
            address=i2c_address,
            port=1,
            cols=16,
            rows=2,
            dotsize=8,
            backlight_enabled=True
        )
        self._input_length = 0
        self._status = "Armed"
        self.reset()

    def reset(self):
        self._input_length = 0
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(" " * 16)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(self._status.ljust(16))

    def key_pressed(self):
        if self._input_length < 16:
            self._input_length += 1
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(("*" * self._input_length).ljust(16))

    def show_denied(self):
        self._input_length = 0
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Wrong Code!     ")
        self._reset_after(2)

    def show_unlocked(self):
        self._input_length = 0
        self._status = "Disarmed"
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(" " * 16)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("Disarmed        ")

    def show_armed(self):
        self._input_length = 0
        self._status = "Armed"
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(" " * 16)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("Armed           ")

    def show_alarm(self):
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("!! ALARM !!")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("Unauthorized!")

    def show_panic(self):
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("!! PANIC !!")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("Help Needed!")

    def show_door_opened(self):
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Door Opened!    ")
        self._reset_after(2)

    def show_doorbell(self):
        self._input_length = 0
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("*Ding Dong!*    ")
        self._reset_after(2)

    def clear_input(self):
        self._input_length = 0
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(" " * 16)

    def _reset_after(self, seconds):
        t = threading.Timer(seconds, self.reset)
        t.daemon = True
        t.start()
