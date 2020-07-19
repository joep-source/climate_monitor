## Used packages
- adafruit-io v2.4.0


## Raspbian configurations
Execute ```$ sudo raspi-config``` to set Serial (no, yes) & I2C.



Execute ```$ sudo nano /boot/config.txt``` and add to the bottom:

```
enable_uart=1
dtoverlay=pi3-disable-bt
```



Execute ```$ sudo chmod 666 /dev/ttyAMA0``` so no longer sudo permission is needed to run (or try ```chmod 777``` and ```serial0```/```ttyS0```).

Execute ```$ sudo chown 777 pi:pi /dev/serial0```.

Check devs via ```$ ls -la /dev/``` + ```serial0```/```ttyS0```/```ttyAMA0```.



Make sure that ```$ sudo nano /boot/cmdline.txt``` contains not ```console=serial0,115200```.