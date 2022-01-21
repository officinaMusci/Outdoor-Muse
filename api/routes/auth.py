import flask

from utils import app
from entities.user import User


blueprint = flask.Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


@blueprint.route('/login', methods=['POST'])
def login():
    '''The API route to get do the login.
    
    RETURNS:
        response: The JSON response containing the access token.
    
    RAISES:
        400 response: Bad request if email or password are not been found.
        401 response: Unauthorized if the user has not been found.
    '''
    request = app.get_request(required_keys=['email', 'password'])

    user = User.get_from_credentials(
        email=request['email'],
        password=request['password']
    )

    if not user:
        flask.abort(401)
    
    return app.response(user.create_access_token())