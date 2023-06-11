# MakeZurich Badge 2023

# Requires:
#  lib/neopixel.mpy
import board
from externalDataProvider import DataProvider
import os
import co2monitor
import time
import batchLeds
import touchio

stateAiring = False

co2monitor = co2monitor.co2monitor()

# GP9, GP19, GP28 and GP14 connect to the touchpad (or a simple wire) and from there it needs
# a 1M Ohm resistor to GND
# see readme for needed extension to be made to the cover in order for this to work
tp1 = touchio.TouchIn(board.GP9)
tp2 = touchio.TouchIn(board.GP19)

leds = batchLeds.batchLeds(board.GP22, 6)
leds.fill(leds.BLACK)
leds.pixels[0] = leds.YELLOW
leds.show()

ledIAQ = 0
ledOAQ = 3
ledDeltaTemp = 2
ledAiringV = 1
ledCallToAction1 = 4
ledCallToAction2 = 5
ledBrightness = 1
ledBrightnessDelta = 0.1

externalDataProvider = DataProvider()
if externalDataProvider.ready():
    print("")
    leds.fill(leds.GREEN)
else:
    leds.fill(leds.RED)
leds.show()
time.sleep(1)
air_quality_data = 0
temperature_outside = 20
last_external_value_update_time = 0

oaqGood = 50
oaqWarning = 150

co2Good = 1000
co2Stop = 500
co2Warning = 1500
co2RateStop = 0.2
co2RateStart = 1.0
co2RateFast = 2.0
stopTime = 0
graceTime = 10

graceTemperature = 5

while True:
    if time.monotonic() - last_external_value_update_time >= 20 and externalDataProvider.ready():
        new_air_quality_data = externalDataProvider.get_air_quality(os.getenv('LATITUDE'), os.getenv('LONGITUDE'))
        # set air quality to 0 if we do not have external data
        if new_air_quality_data:
            air_quality_data = new_air_quality_data
        else:
            air_quality_data = 0
        print("Air quality: ", air_quality_data)

        new_temperature_outside = externalDataProvider.get_current_temperature(os.getenv('LATITUDE'), os.getenv('LONGITUDE'))
        # set outside temperature to the inside temperature if we do not have external data
        if new_temperature_outside:
            temperature_outside = new_temperature_outside
        else:
            temperature_outside = co2monitor.temperature()
        print("Outside temperature: ", temperature_outside)
        last_external_value_update_time = time.monotonic()
    elif not externalDataProvider.ready():
        new_temperature_outside = co2monitor.temperature()


    co2monitor.update()
    print("CO2:", co2monitor.co2(),", rate:",co2monitor.co2Rate(), ", state:",stateAiring)

    if stateAiring:
        
        if co2monitor.co2() < co2Stop:
            stateAiring = False
            print("Stopped airing, co2 ok")
            stopTime = time.monotonic()
            # set lüften led to DONE
            leds.setPixel(ledCallToAction1, leds.GREEN)
            leds.setPixel(ledCallToAction2, leds.GREEN)
        
        elif co2monitor.co2Rate() > -co2RateStop: # stop airing, because not efficient. negative rate!
            stateAiring = False
            print("Stopped airing, rate too low")
            stopTime = time.monotonic()
            # set lüften led to DONE
            leds.setPixel(ledCallToAction1, leds.GREEN)
            leds.setPixel(ledCallToAction2, leds.GREEN)

        elif air_quality_data > oaqWarning: # do not air if OAQ unhealthy
            stateAiring = False
            print("Stopped airing, bad OAQ")
            stopTime = time.monotonic()
            # set lüften led to DONE
            leds.setPixel(ledCallToAction1, leds.GREEN)
            leds.setPixel(ledCallToAction2, leds.GREEN)

        else:
            print("Airing in progress")
            # set lüften led to IN-PROGRESS
            leds.setPixel(ledCallToAction1, leds.BLUE)
            leds.setPixel(ledCallToAction2, leds.BLUE)

        
        if (co2monitor.co2Rate() < -co2RateFast):
            # set rate Led to GREEN, fast improving
            leds.setPixel(ledAiringV, leds.GREEN)
        elif(co2monitor.co2Rate() < 0):
            # set rate Led to YELLOW, not really improving
            leds.setPixel(ledAiringV, leds.YELLOW)
        else:
            # set rate Led to RED, even worsening
            leds.setPixel(ledAiringV, leds.RED)

    else: # not airing

        if co2monitor.co2() > co2Good:

            if co2monitor.co2Rate() < -co2RateStart: # negative rate!
                stateAiring = True
                print("Open window detected, rate=",co2monitor.co2Rate())
                # set lüften led to CALL-TO-ACTION
                leds.setPixel(ledCallToAction1, leds.BLUE)
                leds.setPixel(ledCallToAction2, leds.BLUE)

            else:
                print("Please open the windows!")
                # set lüften led to IN-PROGRESS
                leds.setPixel(ledCallToAction1, leds.RED)
                leds.setPixel(ledCallToAction2, leds.RED)

        else:
            if (time.monotonic() - stopTime) > graceTime:
                # set lüften led to OFF
                leds.setPixel(ledCallToAction1, leds.BLACK)
                leds.setPixel(ledCallToAction2, leds.BLACK)


        if (co2monitor.co2Rate() < -co2RateStart):
            # set rate Led to GREEN, fast improving
            leds.setPixel(ledAiringV, leds.GREEN)
        elif(co2monitor.co2Rate() > co2RateStart):
            # set rate Led to RED, fast decreasing
            leds.setPixel(ledAiringV, leds.RED)
        else:
            # set rate Led to BLACK
            leds.setPixel(ledAiringV, leds.BLACK)



    if co2monitor.co2() < co2Good:
        # set IAQ Led to GREEN
        leds.setPixel(ledIAQ, leds.GREEN)

    elif co2monitor.co2() < co2Warning:
        # set IAQ Led to YELLOW
        leds.setPixel(ledIAQ, leds.YELLOW)

    else:
        # set IAQ Led to RED
        leds.setPixel(ledIAQ, leds.RED)

    
    if air_quality_data <= oaqGood:
        # set OAQ Led to GREEN
        leds.setPixel(ledOAQ, leds.GREEN)

    elif air_quality_data <= oaqWarning:
        # set OAQ Led to YELLOW
        leds.setPixel(ledOAQ, leds.YELLOW)

    else:
        # set OAQ Led to RED
        leds.setPixel(ledOAQ, leds.RED)


    if (co2monitor.temperature() > temperature_outside + graceTemperature ):
        # set deltaTemp Led to BLUE, outside is cold
        leds.setPixel(ledDeltaTemp, leds.BLUE)
    elif (co2monitor.temperature() < temperature_outside - graceTemperature):
        # set deltaTemp Led to RED, outside is hot
        leds.setPixel(ledDeltaTemp, leds.RED)
    else:
        # set deltaTemp Led to GREEN, +/-same
        leds.setPixel(ledDeltaTemp, leds.GREEN)


    # update UI brightness with touchbuttons
    # do not touch on startup!
    if (tp1.value):
        ledBrightness += ledBrightnessDelta
        if ledBrightness <= 0:
            ledBrightness = ledBrightnessDelta
        leds.updateBrightness(ledBrightness)

    elif (tp2.value):
        ledBrightness -= ledBrightnessDelta
        if ledBrightness >= 1.0:
            ledBrightness = 1.0 -ledBrightnessDelta
        leds.updateBrightness(ledBrightness)


    leds.show()
    time.sleep(1)
