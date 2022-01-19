import os

import flask

from utils import app


blueprint = flask.Blueprint(
    'root',
    __name__,
    url_prefix='/'
)


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    '''The home route

    This route is mainly useful for pings.
    
    RETURNS:
        response: An empty JSON response.
    '''
    return app.response()


@blueprint.route('/favicon.ico')
def favicon():
    '''The favicon route.
    
    RETURNS:
        response: The favicon.
    '''
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )