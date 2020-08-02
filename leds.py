import RPi.GPIO as GPIO

LED_R = 29
LED_Y = 31
LED_G = 33

def setup():
    GPIO.setmode(GPIO.BOARD)
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
    if not led:
        GPIO.output(LED_R, GPIO.HIGH)
        GPIO.output(LED_Y, GPIO.HIGH)
        GPIO.output(LED_G, GPIO.HIGH)
    else:
        GPIO.output(led, GPIO.HIGH)
        
