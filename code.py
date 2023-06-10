# MakeZurich Badge 2023

# Requires:
#  lib/neopixel.mpy
from externalDataProvider import DataProvider
import os
import co2monitor
import time

stateAiring = False

co2monitor = co2monitor.co2monitor()

latitude = "47.409008755184594"
longitude = "8.549467354287557"

externalDataProvider = DataProvider()
air_quality_data = externalDataProvider.get_air_quality(latitude, longitude)
last_external_value_update_time = time.monotonic()

oaqGood = 50
oaqWarning = 150

co2Good = 1000
co2Stop = 500
co2Warning = 1500
co2RateStop = -0.2
co2RateStart = -1.0

while True:

    if time.monotonic() - last_external_value_update_time >= 20:
        air_quality_data = externalDataProvider.get_air_quality(latitude, longitude)
        print(air_quality_data)
        forecast_data = externalDataProvider.get_current_temperature(latitude, longitude)
        print(forecast_data)
        last_external_value_update_time = time.monotonic()

    co2monitor.update()

    if stateAiring:
        
        if co2monitor.co2() < co2Stop:
            stateAiring = False
            # set lüften led to DONE
        
        elif co2monitor.co2Rate() < co2RateStop: # stop airing, because not efficient
            stateAiring = False
            # set lüften led to DONE

        elif air_quality_data > oaqWarning: # do not air if OAQ unhealthy
            stateAiring = False
            # set lüften led to DONE

        else:
            pass
            # set lüften led to IN-PROGRESS

    else: # not airing

        if co2monitor.co2() > co2Good:

            if co2monitor.co2Rate() > co2RateStart:
                stateAiring = True
                # set lüften led to CALL-TO-ACTION

            else:
                pass
                # set lüften led to IN-PROGRESS

        else:
            pass
            # set lüften led to OFF


    if co2monitor.co2() < co2Good:
        pass
        # set IAQ Led to GREEN

    elif co2monitor.co2() < co2Warning:
        pass
        # set IAQ Led to YELLOW

    else:
        pass
        # set IAQ Led to RED

    
    if air_quality_data <= oaqGood:
        pass
        # set OAQ Led to GREEN

    elif air_quality_data <= oaqWarning:
        pass
        # set OAQ Led to YELLOW

    else:
        pass
        # set OAQ Led to RED

    
    # set dTemp Led to fct(co2monitor.temp()?, outdoor_temp()?)
