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
last_external_value_update_time = time.monotonic()


GOOD = 0
WARNING = 1
ALERT = 2
def outdoorAirQuality():
    return GOOD

while True:

    if time.monotonic() - last_external_value_update_time >= 20:
        air_quality_data = externalDataProvider.get_air_quality(latitude, longitude)
        print(air_quality_data)
        forecast_data = externalDataProvider.get_weather_forcast(latitude, longitude)
        print(forecast_data)
        last_run_time = time.monotonic()

    co2monitor.update()

    if stateAiring:
        
        if co2monitor.co2() < 500:
            stateAiring = False
            # set lüften led to DONE
        
        elif co2monitor.co2Rate() < -0.2:
            stateAiring = False
            # set lüften led to DONE

        elif outdoorAirQuality() == ALERT:
            stateAiring = False
            # set lüften led to DONE

        else:
            pass
            # set lüften led to IN-PROGRESS

    else: # not airing

        if co2monitor.co2() > 1000:

            if co2monitor.co2Rate() > 1:
                stateAiring = True
                # set lüften led to CALL-TO-ACTION

            else:
                pass
                # set lüften led to IN-PROGRESS

        else:
            pass
            # set lüften led to OFF


    if co2monitor.co2() < 1000:
        pass
        # set IAQ Led to GREEN

    elif co2monitor.co2() < 1500:
        pass
        # set IAQ Led to YELLOW

    else:
        pass
        # set IAQ Led to RED

    
    if outdoorAirQuality() == GOOD:
        pass
        # set OAQ Led to GREEN

    elif outdoorAirQuality() == ALERT:
        pass
        # set OAQ Led to YELLOW

    else:
        pass
        # set OAQ Led to RED

    
    # set dTemp Led to fct(co2monitor.temp()?, outdoor_temp()?)
