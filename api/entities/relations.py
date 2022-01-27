from sqlalchemy import Column as ORMColumn
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import ForeignKey

from services import database


class QueryPlaceRow(database.Base):
    '''ORM association between queries and resulting places'''
    __tablename__ = 'query_place_relation'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    
    query_id = ORMColumn(ForeignKey('query.id'), nullable=False)
    place_id = ORMColumn(ForeignKey('place.id'), nullable=False)


class QueryPartnerRow(database.Base):
    '''ORM association between queries and resulting partners'''
    __tablename__ = 'query_partner_relation'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    
    query_id = ORMColumn(ForeignKey('query.id'), nullable=False)
    partner_id = ORMColumn(ForeignKey('partner.id'), nullable=False)