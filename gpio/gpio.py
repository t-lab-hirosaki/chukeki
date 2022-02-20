# coding: utf-8
import RPi.GPIO as GPIO
import time


class L_chika():
    def __init__(self, pin_num):
        self.pin_num = pin_num
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_num,GPIO.OUT)

    def on(self):
        GPIO.output(self.pin_num,GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin_num,GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()


def main():
    test = L_chika(40)
    test.on()
    time.sleep(1)
    test.off()
    del test

if __name__ == "__main__":
    main()
