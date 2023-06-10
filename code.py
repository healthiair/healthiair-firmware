# MakeZurich Badge 2023

# Requires:
#  lib/neopixel.mpy
from externalDataProvider import DataProvider
import os
import co2monitor
import time

co2monitor = co2monitor.co2monitor()

latitude = "47.409008755184594"
longitude = "8.549467354287557"

externalDataProvider = DataProvider()
last_external_value_update_time = time.monotonic()

while True:
    if time.monotonic() - last_external_value_update_time >= 20:
        air_quality_data = externalDataProvider.get_air_quality(latitude, longitude)
        print(air_quality_data)
        forecast_data = externalDataProvider.get_weather_forcast(latitude, longitude)
        print(forecast_data)
        last_run_time = time.monotonic()
    if co2monitor.dataReady():
        print(co2monitor.co2Rate())

