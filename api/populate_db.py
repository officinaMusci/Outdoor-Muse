import random
from entities.user import User
from entities.place import Place
from entities.partner import Partner
from entities.query import Query
from entities.review import Review


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
for x in range(100):
    User.generate_random().save()

# Generate partners
for x in range(100):
    Partner.generate_random().save()

# Get normal users
users = User.get_all(filter_by={'role': 'user'})

# Get places and partners
places = Place.get_all()
partners = Partner.get_all()

# Generate queries
for user in users:
    for x in range(100):
        query = Query.generate_random()
        query.user_id = user.id
        query.save()
        query.associate_place_row(random.choice(places).id)
        query.associate_partner_row(random.choice(partners).id)

# Generate place reviews
for user in users:
    for x in range(50):
        review = Review.generate_random()
        review.user_id = user.id
        review.place_id = random.choice(places).id

# Generate partner reviews
for user in users:
    for x in range(50):
        review = Review.generate_random()
        review.user_id = user.id
        review.partner_id = random.choice(partners).id