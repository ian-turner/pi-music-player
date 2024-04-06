#!/bin/bash

# update the system
sudo apt-get update
sudo apt-get upgrade -y

# install packages
sudo apt-get install sox i2c-tools python3-pip git -y

# installs pip module for display
sudo pip install git+https://github.com/adafruit/Adafruit_Python_SSD1306.git

# manually enable i2c and audio out
sudo raspi-config

# reboot the system
sudo reboot now
