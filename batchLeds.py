import neopixel

class batchLeds:

    def __init__(self, pin, num):
        self.brightness = 1.0
        self.pixels = neopixel.NeoPixel(pin, num, brightness=self.brightness, auto_write=False)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 150, 0)
        self.GREEN = (0, 255, 0)
        self.CYAN = (0, 255, 255)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (180, 0, 255)
        self.BLACK = (0, 0, 0)


    def setPixel(self, num, color):
        self.pixels[num] = color


    def fill(self, color):
        self.pixels.fill(color)


    def updateBrightness(self, brightness):
        self.pixels.brightness = brightness


    def show(self):
        self.pixels.show()