"""
Module for interacting with Adafruit OLED display
and any LEDs connected to the system
"""

import Adafruit_SSD1306
from gpiozero import LED

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


I2C_BUS = 0
ON_LED_PIN = 12


class Display:
    def __init__(self):
        # setting up output variables
        self.message = ''
        self.time_sec = 0
        self.playing = False

        # initializing display
        try:
            print('Trying to initialize OLED display')
            self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=I2C_BUS)
            self.disp.begin()
            self.disp.clear()
            self.disp.display()
            print('Done')
        except:
            print('Error: could not initialize OLED display')
            self.disp = None

        # initializing on led
        self.on_led = LED(ON_LED_PIN)
        self.on_led.on()


    def clear(self):
        if self.disp:
            self.disp.clear()
            self.disp.display()


    def update(self):
        if self.disp:
            # initialize an image
            width = self.disp.width
            height = self.disp.height
            image = Image.new('1', (width, height))

            # drawing background and text
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()

            draw.rectangle((0,0,width,height), outline=0, fill=0) # black box - for background
            draw.rectangle((0,0,width,height/4), outline=0, fill=255) # yellow rectangle - for outline
            draw.rectangle((2,2,width-2,height/4-2), outline=0, fill=0) # black rectangle - for fill
            draw.rectangle((0,0,(self.time_sec / self.song_time_sec)*width,height/4), outline=0, fill=255)

            # drawing info text on screen
            draw.text((0,8), self.message, font=font, fill=255)
            draw.text((0,16), 'Track %d - %d:%d' % (self.current_song,
                      int(self.time_sec / 60), self.time_sec % 60), font=font, fill=255)

            self.disp.image(image)
            self.disp.display()


    def close(self):
        self.clear()
        self.disp = None
        self.on_led.off()
