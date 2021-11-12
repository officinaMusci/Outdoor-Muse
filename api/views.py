import os

import flask

from app import app, app_response
import crud


@app.route('/', methods=['GET', 'POST'])
def home():
    '''The home route

    This route is mainly useful for pings.
    
    RETURNS:
        response: An empty JSON response.
    '''
    return app_response()


@app.route('/favicon.ico')
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


@app.route('/api/v1/execute-query', methods=['POST'])
def execute_query():
    '''The API route to get query results.
    
    RETURNS:
        response: The JSON response containing the results.
    
    RAISES:
        400 response: Bad request if the search query has not been found.
    '''
    request_dict = flask.request.get_json()

    if not request_dict:
        flask.abort(400)
    
    results = crud.execute_query(request_dict)
    
    return app_response(results)


@app.errorhandler(Exception)
def error(e):
    '''The error route for all handled errors.
    
    ARGS:
        e: The error raised.
    RETURNS:
        response: The JSON response for the error.
    '''
    return app_response(None, e)