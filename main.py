import time
import json
import logging
import mh_z19
import bme280
from Adafruit_IO import Client, Feed, RequestError

ADAFRUIT_IO_KEY = 'e0ee94aa282142709e4acbde576cfd8f'
ADAFRUIT_IO_USERNAME = 'joepleonardo'

LOG_FILE_NAME = 'logs.log'
LOG_LEVEL = logging.WARNING # logging.INFO

ERROR_VALUE = 9999

# Global AIO values
co2_feed = 0
#co2t_feed = 0
temp_feed = 0
humidity_feed = 0
pressure_feed = 0


def sample_avg(time_total_sec, time_sample_sec):
    total_time = time_total_sec
    sleep_time = time_sample_sec
    no_samples = int(total_time/sleep_time)
    sample = {'co2': 0.0,
              'co2_temp': 0.0,
              'temp': 0.0,
              'humidity': 0.0,
              'pressure': 0.0
              }
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
                logging.error('mhz19 error, round '+str(round))
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
    logging.info('co2:      ' + str(sample['co2']))
    logging.info('co2 temp: ' + str(sample['co2_temp']))
    logging.info('temp:     ' + str(sample['temp']))
    logging.info('humidity: ' + str(sample['humidity']))
    logging.info('pressure: ' + str(sample['pressure']))
    return sample


def setup_aio():
    # Create an instance of the REST client
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    logging.info('initialized AdafuitIO')

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
    logging.debug('sending sample start')
    send_to_aio(aio, co2_feed.key,  sample['co2'])
    #send_to_aio(aio, co2t_feed.key, sample['co2_temp'])
    send_to_aio(aio, temp_feed.key, sample['temp'])
    send_to_aio(aio, humidity_feed.key, sample['humidity'])
    send_to_aio(aio, pressure_feed.key, sample['pressure'])
    logging.info('sending sample complete')


def init_logger():
    logging.basicConfig(filename=LOG_FILE_NAME, level=LOG_LEVEL, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('initialized logger')


init_logger()
bme280.setup_all()
logging.info('initialized bme280')
aio = setup_aio()

while True:
    try:
        sample = sample_avg(60, 6)
        send_sample(aio, sample)
    except:
        logging.error('main loop')
        time.sleep(10)

