# MakeZurich Badge 2023

# Requires:
#  lib/neopixel.mpy
import air_quality
import weather_forcast
import wifi
import socketpool
import os
import co2monitor
import time

co2monitor = co2monitor.co2monitor()

latitude = "47.409008755184594"
longitude = "8.549467354287557"

last_external_value_update_time = time.monotonic()

wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)

print("Connected to WiFi")

while True:
    if time.monotonic() - last_external_value_update_time >= 20:
        air_quality_data = air_quality.get_air_quality(pool, latitude, longitude)
        print(air_quality_data)
        forecast_data = weather_forcast.get_weather_forcast(pool, latitude, longitude)
        print(forecast_data)
        last_run_time = time.monotonic()
    if co2monitor.dataReady():
        print(co2monitor.co2Rate())

