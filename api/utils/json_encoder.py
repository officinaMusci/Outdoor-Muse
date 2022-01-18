from datetime import datetime, timedelta

from flask.json import JSONEncoder

from utils import time


class CustomJSONEncoder(JSONEncoder):
    '''Custom JSON encoder for Flask'''
    def default(self, obj):
        '''Fix the datetime and timedelta conversions'''
        try:
            if isinstance(obj, datetime):
                return obj.strftime(time.datetime_format())
            elif isinstance(obj, timedelta):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)