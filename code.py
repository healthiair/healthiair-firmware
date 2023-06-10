# MakeZurich Badge 2023

# Requires:
#  lib/neopixel.mpy
import board
from externalDataProvider import DataProvider
import os
import co2monitor
import time
import batchLeds

stateAiring = False

co2monitor = co2monitor.co2monitor()

leds = batchLeds.batchLeds(board.GP22, 6)
ledIAQ = 0
ledOAQ = 3
ledDeltaTemp = 2
ledAiringV = 1
ledCallToAction1 = 4
ledCallToAction2 = 5

latitude = "47.409008755184594"
longitude = "8.549467354287557"

externalDataProvider = DataProvider()
air_quality_data = 0
last_external_value_update_time = time.monotonic()

oaqGood = 50
oaqWarning = 150

co2Good = 1000
co2Stop = 500
co2Warning = 1500
co2RateStop = -0.2
co2RateStart = -1.0
stopTime = 0
graceTime = 10

while True:

    if time.monotonic() - last_external_value_update_time >= 20:
        air_quality_data = externalDataProvider.get_air_quality(latitude, longitude)
        print(air_quality_data)
        forecast_data = externalDataProvider.get_current_temperature(latitude, longitude)
        print(forecast_data)
        last_external_value_update_time = time.monotonic()

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
        
        elif co2monitor.co2Rate() > co2RateStop: # stop airing, because not efficient. negative rate!
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

    else: # not airing

        if co2monitor.co2() > co2Good:

            if co2monitor.co2Rate() < co2RateStart: # negative rate!
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

    # set dTemp Led to fct(co2monitor.temp()?, outdoor_temp()?)

    leds.show()
    time.sleep(1)
