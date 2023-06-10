import adafruit_requests
import ssl
import os
import wifi
import socketpool


class DataProvider:
    def __init__(self):
        try:
            wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
            self._pool = socketpool.SocketPool(wifi.radio)
            self._wifi_connected = True
            print("Connected to WiFi")
        except:
            self._wifi_connected = False

    def get_current_temperature(self, lat, lng):
        if not self._wifi_connected:
            return

        requests = adafruit_requests.Session(self._pool, ssl.create_default_context())

        url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lng + '&hourly=temperature_2m,rain&current_weather=true&forecast_days=1'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['current_weather']['temperature']
        else:
            print('Request failed:', response.status_code)
        response.close()

    def get_air_quality(self, lat, lng):
        if not self._wifi_connected:
            return

        requests = adafruit_requests.Session(self._pool, ssl.create_default_context())

        url = 'http://api.waqi.info/feed/geo:' + lat + ';+' + lng + '/?token=' + os.getenv('AQI_TOKEN')
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['data']['aqi']
        else:
            print('Request failed:', response.status_code)
        response.close()

    def ready(self):
        return self._wifi_connected
