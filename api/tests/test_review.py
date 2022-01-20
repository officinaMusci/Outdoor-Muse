import os
import unittest

from entities.user import User
from entities.place import Place
from entities.partner import Partner
from entities.review import Review


class TestReview(unittest.TestCase):
    '''Tests the Review object'''

    def delete_db(self):
        '''Delete test database file'''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    

    def create_review_with_relations(self):
        user = User.generate_random()
        user_id = user.save()

        place = Place.generate_random()
        place_id = place.save()

        partner = Partner.generate_random()
        partner_id = partner.save()

        parent = Review.generate_random()
        parent.user_id = user_id
        parent.place_id = place_id
        parent.partner_id = partner_id
        parent_id = parent.save()

        review = Review.generate_random()
        review.user_id = user_id
        review.place_id = place_id
        review.partner_id = partner_id
        review.parent_id = parent_id
        review_id = review.save()

        return Review.get_from_id(review_id)


    def setUp(self):
        '''Initialize the test'''
        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_review.sqlite'
        )

        self.delete_db()
        
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"


    def test_create(self):
        '''Tests the creation in the database'''
        review = Review.generate_random()
        review_id = review.save()
        
        retrieved_review = Review.get_from_id(review_id)
        self.assertEqual(review, retrieved_review)


    def test_relations(self):
        '''Tests the relations in the database'''
        review = self.create_review_with_relations()

        retrieved_user = User.get_from_id(review.user_id)
        self.assertIsNotNone(retrieved_user)

        retrieved_place = Place.get_from_id(review.place_id)
        self.assertIsNotNone(retrieved_place)

        retrieved_partner = Partner.get_from_id(review.partner_id)
        self.assertIsNotNone(retrieved_partner)

        retrieved_parent = Review.get_from_id(review.parent_id)
        self.assertIsNotNone(retrieved_parent)

        # On user deletion, the review should be anonymous
        review = self.create_review_with_relations()
        User.get_from_id(review.user_id).delete()
        self.assertIsNotNone(Review.get_from_id(review.id))

        # On place deletion, the review should be deleted
        review = self.create_review_with_relations()
        Place.get_from_id(review.place_id).delete()
        self.assertIsNone(Review.get_from_id(review.id))
        
        # On partner deletion, the review should be deleted
        review = self.create_review_with_relations()
        Partner.get_from_id(review.partner_id).delete()
        self.assertIsNone(Review.get_from_id(review.id))
        
        # On parent deletion, the review should be deleted
        review = self.create_review_with_relations()
        Review.get_from_id(review.parent_id).delete()
        self.assertIsNone(Review.get_from_id(review.id))


    def test_update(self):
        '''Tests the update in the database'''
        review = Review.generate_random()
        review_id = review.save()

        review_2 = Review.generate_random()
        review_id_2 = review_2.save()

        review_2.content = 'My review 2'
        review_2.points = 1001

        review_2.save()

        retrieved_review = Review.get_from_id(review_id)
        retrieved_review_2 = Review.get_from_id(review_id_2)

        self.assertNotEqual(retrieved_review, retrieved_review_2)


    def test_delete(self):
        '''Tests the deletion from the database'''
        review = Review.generate_random()
        review_id = review.save()

        review_2 = Review.generate_random()
        review_id_2 = review_2.save()
        review_2.delete()

        retrieved_review = Review.get_from_id(review_id)
        retrieved_review_2 = Review.get_from_id(review_id_2)

        self.assertIsNotNone(retrieved_review)
        self.assertIsNone(retrieved_review_2)


    def tearDown(self):
        '''Finalise the test removing the test database file'''
        #self.delete_db()