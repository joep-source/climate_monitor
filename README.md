## Raspbian configurations
Execute ```$ sudo raspi-config``` to set Serial (no, yes) & I2C


Execute ```$ sudo nano /boot/config.txt```
And add to the bottom:
```enable_uart=1
dtoverlay=pi3-disable-bt```


Execute ```$ sudo chmod 666 /dev/ttyAMA0``` so no longer sudo permission is needed to run.
