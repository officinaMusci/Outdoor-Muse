import flask

from utils import app
from entities.user import User


blueprint = flask.Blueprint(
    'users',
    __name__,
    url_prefix='/users'
)

@blueprint.route('/', methods=['GET'])
@app.jwt_required(roles=['admin'])
def get():
    ''''''
    users = User.get_all(flask.request.args.to_dict())
    app.response([users])