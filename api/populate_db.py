from datetime import datetime, timedelta,  timezone
import random
from random import randrange

from entities.user import User
from entities.place import Place
from entities.partner import Partner
from entities.query import Query
from entities.review import Review

from utils import time
from services import database


# Entity generator
def generate_in_the_past(entityClass):
    created = time.random_datetime(
        start=(
            datetime.now(timezone.utc)
            - timedelta(days=randrange(100))
        ),
        end=datetime.now(timezone.utc)
    )

    entity = entityClass.generate_random()
    entity.created = created
    entity.updated = created

    return entity


# Query generator
def generate_query(user:User=None) -> Query:
    query = generate_in_the_past(Query)
    query.user_id = user.id if user else None
    query.save()
    
    for x in range(randrange(100)):
        query.associate_place_row(random.choice(places).id)
    
    for x in range(randrange(100)):
        query.associate_partner_row(random.choice(partners).id)
    
    return query

'''
# Drop all database tables
#with database.create_session().begin() as db_session:
#    database.Base.metadata.drop_all(db_session.get_bind())
#    db_session.close()

# Generate admin
admin = User(
    email='admin@test.test',
    password='test_password',
    confirmed=True,
    role='admin',
    name='Admin de Testis'
)
admin.save()

# Generate users
for x in range(randrange(1000, 1500)):
    generate_in_the_past(User).save()

# Generate partners
for x in range(randrange(500, 1000)):
    generate_in_the_past(Partner).save()
'''
# Get activated normal users
users = User.get_all(filter_by={
    'role': 'user',
    'confirmed': True
})

# Get places and partners
places = Place.get_all()
partners = Partner.get_all()
'''
# Generate user queries
for user in users:
    for x in range(randrange(100)):
        generate_query(user).save()
'''
# Generate anonymous queries
for x in range(randrange(1000, 5000)):
    generate_query().save()

# Generate place reviews
for user in users:
    for x in range(randrange(50)):
        review = generate_in_the_past(Review)
        review.user_id = user.id
        review.place_id = random.choice(places).id
        review.save()

# Generate partner reviews
for user in users:
    for x in range(randrange(50)):
        review = generate_in_the_past(Review)
        review.user_id = user.id
        review.partner_id = random.choice(partners).id
        review.save()