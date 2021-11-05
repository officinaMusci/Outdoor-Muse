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
    'type': 'natural_feature',
    'max_travel': '2:30:00',
    'max_walk': '0:30:00',
    'weather_ids': [
		301,
		615,
		800
	],
	'max_results': 5
}

# Based on the Google Place API response
PLACE_DICT = {
    'business_status': 'OPERATIONAL',
	'geometry': {
		'location': {
			'lat': 46.2101227,
			'lng': 6.1441002
		},
		'viewport': {
			'northeast': {
				'lat': 46.21137253029151,
				'lng': 6.145228730291502
			},
			'southwest': {
				'lat': 46.20867456970851,
				'lng': 6.142530769708498
			}
		}
	},
	'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/bar-71.png',
	'icon_background_color': '#FF9E67',
	'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/bar_pinlet',
	'name': 'Les Brasseurs',
	'opening_hours': {
		'open_now': True
	},
	'photos': [{
		'height': 1080,
		'html_attributions': ['<a href="https://maps.google.com/maps/contrib/101388297625767099028">Les Brasseurs</a>'],
		'photo_reference': 'Aap_uECFPHut2kuclDOigjLqF2z9kqzwtYy2k_1N6HECW-kHaYBNHFI9QWfq_AOz_xD4i6S70m28Y-ikrSXT2LkhdoRp7axijMyxhrmH0aHG-1LCTp0BH_99GgTRfPIFpEuhxnpZ58RrhkkJSaj0Otx3lX2BEt928iWCVrrcds_moqOemXKw',
		'width': 1619
	}],
	'place_id': 'ChIJK0l2EidljEcRNacaci8fCTE',
	'plus_code': {
		'compound_code': '646V+2J Geneva, Switzerland',
		'global_code': '8FR8646V+2J'
	},
	'price_level': 2,
	'rating': 4.1,
	'reference': 'ChIJK0l2EidljEcRNacaci8fCTE',
	'scope': 'GOOGLE',
	'types': ['bar', 'meal_takeaway', 'restaurant', 'food', 'point_of_interest', 'establishment'],
	'user_ratings_total': 1113,
	'vicinity': 'Place de Cornavin 20, Genève'
}