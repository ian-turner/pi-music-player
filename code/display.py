import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Display:
    def __init__(self):
        # initializing display
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

    def clear(self):
        self.disp.clear()
        self.disp.display()

    def write(self, _text: str):
        # initialize an image
        width = self.disp.width
        height = self.disp.height
        image = Image.new('1', (width, height))

        # drawing background and text
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((0,10), _text, font=font, fill=255)

        self.disp.image(image)
        self.disp.display()
