import flask

from utils import app
from entities.review import Review


blueprint = flask.Blueprint(
    'reviews',
    __name__,
    url_prefix='/reviews'
)


@blueprint.route('', methods=['GET', 'POST'])
@app.jwt_required(roles=['admin'])
def get():
    '''The API route to get or create the reviews.
    
    RETURNS:
        response: The JSON response containing the reviews or the created review.
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the review hasn't one of the required roles.
    '''
    request = app.get_request()

    if flask.request.method == 'GET':
        reviews = Review.get_all(request)
        return app.response(reviews)
    
    elif flask.request.method == 'POST':
        review = Review.from_dict(request)
        review.save()
        return app.response([review])


@blueprint.route('/<review_id>', methods=['GET', 'DELETE', 'PUT'])
@app.jwt_required(roles=['admin'])
def get_one(review_id):
    '''The API route to get, delete or update a review.
    
    RETURNS:
        response: The JSON response containing the review (True if deleted).
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the review hasn't one of the required roles.
    '''
    review = Review.get_from_id(review_id)

    if flask.request.method == 'GET':
        return app.response(review)
    
    elif flask.request.method == 'DELETE':
        return app.response(review.delete())
    
    elif flask.request.method == 'PUT':
        request = app.get_request()

        updated_review = Review.from_dict(request)
        updated_review.id = review_id
        updated_review.save()
        
        return app.response(updated_review)