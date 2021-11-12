from datetime import datetime, timedelta, timezone

from utils import time


datetime_format = time.datetime_format()

datetime_start = datetime.now(timezone.utc).replace(hour=9, minute=0, second=0) + timedelta(days=1)
datetime_end = datetime_start + timedelta(hours=10)


QUERY_DICT = {
    'location': {
        'lat': 46.204391,
        'lng': 6.143158
    },
    'interval': {
        'start': datetime_start.strftime(datetime_format),
        'end': datetime_end.strftime(datetime_format)
    },
    'radius': 150000,
    'type': 'hike',
    'max_travel': '4:00:00',
    'max_walk': '2:00:00',
    'weather_ids': [
		301,
		615,
		800
	],
	'max_results': 10
}

PLACE_DICT = {
	'name': 'Auf den Spuren von Alix',
	'duration': '3:00:00',
	'distance': 10500,
	'difficulty': 1,
	'location': {
		'lat': 9.2754524816615,
		'lng': 46.791814126484
	},
	'types': [
		'hike'
	]
}