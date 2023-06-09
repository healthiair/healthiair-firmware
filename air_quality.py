import adafruit_requests
import ssl
import os

def get_air_quality(pool,lat,lng):
    
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    url = 'http://api.waqi.info/feed/geo:'+lat+';+'+lng+'/?token='+os.getenv('AQI_TOKEN')
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Request failed:', response.status_code)