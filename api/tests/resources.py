from datetime import datetime, timedelta, timezone

from utils import time


datetime_format = time.datetime_format()

datetime_start = datetime.now(timezone.utc)
datetime_end = datetime_start + timedelta(days=7)


QUERY_DICT = {
    'location': {
        'lat': 46.204391,
        'lng': 6.143158
    },
    'interval': {
        'start': datetime_start.strftime(datetime_format),
        'end': datetime_end.strftime(datetime_format)
    },
    'radius': 100000,
    'type': 'hike',
    'max_travel': '2:30:00',
    'max_walk': '0:30:00',
    'weather_ids': [
		301,
		615,
		800
	],
	'max_results': 5
}

PLACE_DICT = {
	'name': 'Auf den Spuren von Alix',
	'notes': None,
	'diff_degree': 'T1',
	'duration': '3:00:00',
	'distance': 10500,
	'diff_level': 1,
	'location': {
		'lat': 9.2754524816615,
		'lng': 46.791814126484
	},
	'types': [
		'hike'
	]
}