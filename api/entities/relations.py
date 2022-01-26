from sqlalchemy import Column as ORMColumn
from sqlalchemy import String as ORMString
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import Float as ORMFloat
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import Interval as ORMInterval
from sqlalchemy import PickleType as ORMPickleType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

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