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


# Drop all database tables
with database.create_session().begin() as db_session:
    database.Base.metadata.drop_all(db_session.get_bind())
    db_session.close()


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
for x in range(randrange(5000, 10000)):
    User.generate_random().save()

# Generate partners
for x in range(randrange(1000, 2000)):
    Partner.generate_random().save()

# Get activated normal users
users = User.get_all(filter_by={
    'role': 'user',
    'activated': True
})

# Get places and partners
places = Place.get_all()
partners = Partner.get_all()

# Query generator
def generate_query(user:User=None) -> Query:
    query_datetime = time.random_datetime(
        start=(
            datetime.now(timezone.utc)
            - timedelta(days=randrange(100))
        ),
        end=datetime.now(timezone.utc)
    )

    query = Query.generate_random()
    query.created = query_datetime
    query.updated = query_datetime
    query.user_id = user.id if user else None
    query.save()
    
    for x in range(randrange(100)):
        query.associate_place_row(random.choice(places).id)
    
    for x in range(randrange(100)):
        query.associate_partner_row(random.choice(partners).id)

# Generate user queries
for user in users:
    for x in range(randrange(1000)):
        generate_query(user)

# Generate anonymous queries
for x in range(randrange(100000, 500000)):
    generate_query()

# Generate place reviews
for user in users:
    for x in range(randrange(500)):
        review = Review.generate_random()
        review.user_id = user.id
        review.place_id = random.choice(places).id
        review.save()

# Generate partner reviews
for user in users:
    for x in range(randrange(500)):
        review = Review.generate_random()
        review.user_id = user.id
        review.partner_id = random.choice(partners).id
        review.save()