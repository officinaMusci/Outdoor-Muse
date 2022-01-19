import os
import requests
import json
from datetime import datetime, timedelta, timezone
from typing import List

from dotenv import load_dotenv

from utils import time
from entities.location import Location
from entities.interval import Interval
from entities.forecast import Forecast


load_dotenv()
api_key=os.getenv('OPENWEATHER_KEY')
language = os.getenv('LANGUAGE')


id_groups = {
    'clear': [800],
    'clouds': [801, 802, 803, 804],
    'snow': [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622],
    'rain': [500, 501, 502, 503, 504, 511, 520, 521, 522, 531],
    'thunderstorm': [200, 201, 202, 210, 211, 212, 221, 230, 231, 232],
    'other': [300, 301, 302, 310, 311, 312, 313, 314, 321, 701, 711, 721, 731, 741, 751, 761, 762, 771, 781]
}


def get_daily_forecasts(
    location:Location,
    interval:Interval=None,
    language:str=language
) -> List[Forecast]:
    '''Gets up to 7 daily forecasts for a given location.

    All conditions available: https://openweathermap.org/weather-conditions
    
    ARGS:
        location: The location for which to obtain the forecasts.
        interval: The interval in which to obtain the forecasts.

    RETURNS:
        forecasts: The list of the available forecasts.
    '''
    if interval:
        max_dt = datetime.now(timezone.utc) + timedelta(days=7)
        assert interval.end <= max_dt, 'Forecasts are available for 7 days only'

    url = 'https://api.openweathermap.org/data/2.5/onecall'
    params = {
        'lat': location.lat,
        'lon': location.lng,
        'appid': api_key,
        'lang': language,
        'units': 'metric',
        'exclude': ','.join(['current', 'minutely', 'hourly', 'alerts'])
    }
    url_params = '&'.join([f"{k}={v}" for k, v in params.items()])
    request_url = f"{url}?{url_params}"

    response = requests.get(request_url)
    data = json.loads(response.text)

    forecasts = []
    for dictionary in data['daily']:
        if interval.contains(
            datetime.fromtimestamp(dictionary['dt'])
        ) or not interval:
            dictionary['location'] = {
                'lat': data['lat'],
                'lng': data['lon']
            }
            forecasts.append(Forecast.from_dict(dictionary))
    
    return forecasts