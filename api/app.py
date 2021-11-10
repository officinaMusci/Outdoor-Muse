import os
import traceback
from datetime import datetime, timedelta

import flask
from flask.json import JSONEncoder
from flask_cors import CORS

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


app = flask.Flask(__name__)
app.json_encoder = CustomJSONEncoder
CORS(app)


is_dev = os.getenv('FLASK_ENV') == 'development'


def app_response(results=None, error=None):
    '''Compose the standard app response.
    
    ARGS:
        results: The results of the request.
        error: The error given by the request.
    RETURNS:
        response: The JSON response.
    '''
    code = 200

    if error:
        code = error.code if hasattr(error, 'code') else 500

        error = {
            'type': type(error).__name__,
            'message': str(error),
        }

        if is_dev:
            error['traceback'] = traceback.format_exc()
            error['code'] = code

    return flask.make_response(
        flask.jsonify({
            'results': results,
            'error': error
        }),
        code
    )


import views