import time
import board
import busio
import adafruit_scd4x

class co2monitor:

    def __init__(self):
        # See badge pinout, depending on the connector you use 
        # you have to select the corresponding GPIOs used for the I2C communication
        # https://github.com/makezurich/makezurich-badge-2023/blob/main/makezurich2023-badge-pinout.png
        # The format is busio.I2C(SCL, SDA)
        # The example below assumes you used I2C1 on the badge
        i2c = busio.I2C(board.GP3, board.GP2)
        self.scd4x = adafruit_scd4x.SCD4X(i2c)
        self.scd4x.start_periodic_measurement()

        while not self.dataReady():
            time.sleep(1)

        initValue = self.scd4x.CO2
        self.co2readings = [initValue for i in range(10)]
        self.co2averages = [initValue for i in range(2)]
        self.timeReadings = [j*4 for j in range(2)]
        self.startTime = time.monotonic()
        self.now = self.startTime


    def dataReady(self):
        return self.scd4x.data_ready


    def mean(self, list):
        return sum(list)/len(list)


    def update(self):
        now = time.monotonic() - self.startTime

        # make measurement
        co2 = self.scd4x.CO2
        self.co2readings = self.co2readings[1:] + [co2]
        self.co2averages = self.co2averages[1:] + [self.mean(self.co2readings)]

        self.timeReadings = self.timeReadings[1:] + [now]
   

    def co2Rate(self):
        self.update()
        return (self.co2averages[-1] - self.co2averages[0])/(self.timeReadings[-1] - self.timeReadings[0])

