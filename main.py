import sys
import time
import json
import logging
import logging.handlers as handlers
from Adafruit_IO import Client, Feed, RequestError
import mh_z19
import bme280
import leds


ADAFRUIT_IO_KEY = 'e0ee94aa282142709e4acbde576cfd8f'
ADAFRUIT_IO_USERNAME = 'joepleonardo'

LOG_FILE_NAME = 'logs/log'
LOG_LEVEL = logging.WARNING # logging.INFO

ERROR_VALUE = 9999

# Global AIO values
co2_feed = 0
#co2t_feed = 0
temp_feed = 0
humidity_feed = 0
pressure_feed = 0

# Global logger
logger = logging.getLogger('my_app')


def sample_avg(total_time, sleep_time):
    no_samples = int(total_time/sleep_time)
    sample = {'co2': 0.0,
              'co2_temp': 0.0,
              'temp': 0.0,
              'humidity': 0.0,
              'pressure': 0.0}
    mh_z19_correct = True
    
    # Sum all samples over time
    for round in range(0, no_samples):
        # Save mh-z19 data
        if (mh_z19_correct):
            try:
                mh_z19_data = mh_z19.read_all()
                sample['co2'] += mh_z19_data['co2']
                sample['co2_temp'] += mh_z19_data['temperature']
            except:
                mh_z19_correct = False
                sample['co2'] = ERROR_VALUE
                sample['co2_temp'] = ERROR_VALUE
                logger.error('mhz19 error, round '+str(round))
        # Save bme280 data
        bme280_data = bme280.real_all_dict()
        sample['temp'] += bme280_data['temperature']
        sample['humidity'] += bme280_data['humidity']
        sample['pressure'] += bme280_data['pressure']
        # Delay
        time.sleep(sleep_time)
        
    # Take average
    for item in sample:
        if (sample[item] != ERROR_VALUE):
            sample[item] = (float)(sample[item])/no_samples
            
    # log sample
    logger.info('co2:      ' + str(sample['co2']))
    logger.info('co2 temp: ' + str(sample['co2_temp']))
    logger.info('temp:     ' + str(sample['temp']))
    logger.info('humidity: ' + str(sample['humidity']))
    logger.info('pressure: ' + str(sample['pressure']))
    return sample, not mh_z19_correct


def setup_aio():
    # Create an instance of the REST client
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    logger.info('initialized AdafuitIO client')

    # Assign the feeds that already exitst, otherwise create and assign them.
    global co2_feed
    global co2t_feed
    global temp_feed
    global humidity_feed
    global pressure_feed
    try:
        co2_feed = aio.feeds('co2')
    except RequestError:
        co2_feed = aio.create_feed(Feed(name='co2'))
    #try:
    #    co2t_feed = aio.feeds('co2_temp')
    #except RequestError:
    #    co2t_feed = aio.create_feed(Feed(name='co2_temp')
    try:
        temp_feed = aio.feeds('temperature')
    except RequestError:
        temp_feed = aio.create_feed(Feed(name='temperature'))
    try:
        humidity_feed = aio.feeds('humidity')
    except RequestError:
        humidity_feed = aio.create_feed(Feed(name='humidity'))
    try:
        pressure_feed = aio.feeds('pressure')
    except RequestError:
        pressure_feed = aio.create_feed(Feed(name='pressure'))

    return aio


def send_to_aio(aio, key, data):
    if (data != ERROR_VALUE):
        # sending data to Adafruit IO
        aio.send(key, data)
        time.sleep(1)


def send_sample(aio, sample):
    logger.debug('sending sample start')
    send_to_aio(aio, co2_feed.key,  sample['co2'])
    #send_to_aio(aio, co2t_feed.key, sample['co2_temp'])
    send_to_aio(aio, temp_feed.key, sample['temp'])
    send_to_aio(aio, humidity_feed.key, sample['humidity'])
    send_to_aio(aio, pressure_feed.key, sample['pressure'])
    logger.info('sending sample complete')


def logger_setup():
    logger.setLevel(LOG_LEVEL)
    logHandler = handlers.TimedRotatingFileHandler(LOG_FILE_NAME, when='midnight', interval=1, backupCount=2)
    logHandler.setLevel(logging.INFO)
    logHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(logHandler)
    logger.info('initialized logger')


# Init everything
leds.setup()
leds.on()
logger.info('initialized leds')
logger_setup()
bme280.setup_all()
logger.info('initialized bme280')
aio = setup_aio()
logger.info('initialized AdafuitIO')

leds.off()
leds.on(leds.LED_G)  # first round with green
while True:
    try:
        sample, error = sample_avg(total_time=60, sleep_time=6)
        send_sample(aio, sample)
        if error:
            leds.on(leds.LED_R)
        else:
            leds.off()
    except KeyboardInterrupt as e:
        leds.off()
        sys.exit(0)
    except Exception as e:
        leds.on(leds.LED_Y)
        logger.error('main loop: ' + str(repr(e)))
        logger.exception('main loop exception')
        time.sleep(10)

