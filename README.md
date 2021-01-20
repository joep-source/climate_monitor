# Room Climate
A Raspberry Pi IoT device to monitor room climate (hobby project). Measures CO2, temperature and humidity.

## Hardware
- Raspberry Pi model 3B
- MH-Z19 sensor
- BME280 sensor
- Leds

## Software
Running Raspbian Buster OS.

### Used packages
- adafruit-io v2.4.0

Included in project:
- bme280 [source](https://github.com/kbrownlees/bme280/tree/master/bme280)
- mh-z19 (modified) [source](https://github.com/UedaTakeyuki/mh-z19/blob/master/mh_z19.py)

### Raspbian configurations
- Execute ```$ sudo raspi-config``` to set Serial (select no, then yes) & I2C.

Troubleshooting MH-Z19 issues:
- Execute ```$ sudo nano /boot/config.txt``` and add to the bottom:
  - ```enable_uart=1```
  - ```dtoverlay=pi3-disable-bt```
- Execute ```$ sudo chmod 666 /dev/ttyAMA0``` to remove sudo permission (or try ```chmod 777``` and ```serial0```/```ttyS0```).
- Execute ```$ sudo chown 777 pi:pi /dev/serial0```.
- Check devs via ```$ ls -la /dev/``` + ```serial0``` / ```ttyS0``` / ```ttyAMA0```.
- Make sure that ```$ sudo nano /boot/cmdline.txt``` contains no ```console=serial0,115200```.