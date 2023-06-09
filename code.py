# MakeZurich Badge 2023

# Requires:
#  lib/neopixel.mpy
import air_quality
import wifi
import socketpool
import os
import co2monitor

co2monitor = co2monitor.co2monitor()

latitude = "47.409008755184594"
longitude = "8.549467354287557"

wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)

print("Connected to WiFi")

data = air_quality.get_air_quality(pool, latitude, longitude)
print(data)
while True:
    if co2monitor.dataReady():
        print(co2monitor.co2Rate())

