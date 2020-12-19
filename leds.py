import RPi.GPIO as GPIO
import datetime as dt

LED_R = 29
LED_Y = 31
LED_G = 33

NIGHT_LEDS_OFF = True
NIGHT_START_HOUR = 23
NIGHT_END_HOUR = 7


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_Y, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    
    
def off(led=None):
    if not led:
        GPIO.output(LED_R, GPIO.LOW)
        GPIO.output(LED_Y, GPIO.LOW)
        GPIO.output(LED_G, GPIO.LOW)
    else:
        GPIO.output(led, GPIO.LOW)
    

def on(led=None):    
    # skip turn leds on at night?
    if NIGHT_LEDS_OFF:
        hour = dt.datetime.now().hour
        if hour>=NIGHT_START_HOUR or hour<NIGHT_END_HOUR:
            return

    # turn leds on
    if not led:
        GPIO.output(LED_R, GPIO.HIGH)
        GPIO.output(LED_Y, GPIO.HIGH)
        GPIO.output(LED_G, GPIO.HIGH)
    else:
        GPIO.output(led, GPIO.HIGH)
