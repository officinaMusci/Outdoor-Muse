import flask

from utils import app
from entities.solution import Solution
from entities.partner import Partner


blueprint = flask.Blueprint(
    'partners',
    __name__,
    url_prefix='/partners'
)


@blueprint.route('', methods=['GET', 'POST'])
@app.jwt_required(roles=['admin'])
def get():
    '''The API route to get or create the partners.
    
    RETURNS:
        response: The JSON response containing the partners or the created partner.
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the partner hasn't one of the required roles.
    '''
    request = app.get_request()

    if flask.request.method == 'GET':
        partners = Partner.get_all(request)
        return app.response(partners)
    
    elif flask.request.method == 'POST':
        partner = Partner.from_dict(request)
        partner.save()
        return app.response(partner)


@blueprint.route('/solution/<solution_id>', methods=['GET'])
def get_for_solution(solution_id):
    '''The API route to get partners for a solution
    
    RETURNS:
        response: The JSON response containing the partners.
    '''
    partners = []
    for partner_id in Solution.get_from_id(solution_id).get_partner_ids():
        partners.append(Partner.get_from_id(partner_id))
        
    return app.response(partners)


@blueprint.route('/<partner_id>', methods=['GET', 'DELETE', 'PUT'])
@app.jwt_required(roles=['admin'])
def get_one(partner_id):
    '''The API route to get, delete or update a partner.
    
    RETURNS:
        response: The JSON response containing the partner (True if deleted).
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the partner hasn't one of the required roles.
    '''
    partner = Partner.get_from_id(partner_id)

    if flask.request.method == 'GET':
        return app.response(partner)
    
    elif flask.request.method == 'DELETE':
        return app.response(partner.delete())
    
    elif flask.request.method == 'PUT':
        request = app.get_request()

        updated_partner = Partner.from_dict(request)
        updated_partner.id = partner_id
        updated_partner.save()
        
        return app.response(updated_partner)