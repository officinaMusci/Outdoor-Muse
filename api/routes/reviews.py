import flask

from utils import app
from entities.review import Review
from entities.user import User
from entities.place import Place
from entities.partner import Partner


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

        for i, review in enumerate(reviews):
            reviews[i].user_name = User.get_from_id(
                review.user_id
            ).name if review.user_id else None

            reviews[i].partner_name = Partner.get_from_id(
                review.partner_id
            ).name if review.partner_id else None
            
            reviews[i].place_name = Place.get_from_id(
                review.place_id
            ).name if review.place_id else None
            

        return app.response(reviews)
    
    elif flask.request.method == 'POST':
        review = Review.from_dict(request)
        review.save()
        return app.response(review)


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