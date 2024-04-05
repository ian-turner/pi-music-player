#!/bin/bash

# update the system
sudo apt-get update
sudo apt-get upgrade -y

# install packages
sudo apt-get install sox i2c-tools python3-pip git -y

# installs pip module for both user and root since
# root pip modules are needed for systemctl service
pip install git+https://github.com/adafruit/Adafruit_Python_SSD1306.git
sudo pip install git+https://github.com/adafruit/Adafruit_Python_SSD1306.git

# update boot config for audio out to GPIO
echo "audio_pwm_mode=2\ndtoverlay=audremap,pins_18_19" | tee -a /boot/config.txt

# now enable i2c and set audio out to headphone jack manually
sudo raspi-config

# reboot system
sudo reboot now
