import adafruit_requests
import ssl


def get_weather_forcast(pool, lat, lng):
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lng + '&hourly=temperature_2m,rain&forecast_days=1'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        response.close()
        return data
    else:
        print('Request failed:', response.status_code)
