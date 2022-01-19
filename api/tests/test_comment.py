import os
import unittest

from entities.user import User, TEST_USER
from entities.place import Place, TEST_PLACE
from entities.partner import Partner, TEST_PARTNER
from entities.comment import Comment, TEST_COMMENT


class TestComment(unittest.TestCase):
    '''Tests the Comment object'''

    def delete_db(self):
        '''Delete test database file'''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    

    def create_comment_with_relations(self):
        user = User.from_dict(TEST_USER)
        user_id = user.save()

        place = Place.from_dict(TEST_PLACE)
        place_id = place.save()

        partner = Partner.from_dict(TEST_PARTNER)
        partner_id = partner.save()

        parent = Comment.from_dict(TEST_COMMENT)
        parent_id = parent.save()

        comment = Comment.from_dict(TEST_COMMENT)
        comment.user_id = user_id
        comment.place_id = place_id
        comment.partner_id = partner_id
        comment.parent_id = parent_id
        comment_id = comment.save()

        return Comment.get_from_id(comment_id)


    def setUp(self):
        '''Initialize the test'''
        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_comment.db'
        )

        self.delete_db()
        
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"


    def test_create(self):
        '''Tests the creation in the database'''
        comment = Comment.from_dict(TEST_COMMENT)
        comment_id = comment.save()
        
        retrieved_comment = Comment.get_from_id(comment_id)
        self.assertEqual(comment, retrieved_comment)


    def test_relations(self):
        '''Tests the relations in the database'''
        comment = self.create_comment_with_relations()

        retrieved_user = User.get_from_id(comment.user_id)
        self.assertIsNotNone(retrieved_user)

        retrieved_place = Place.get_from_id(comment.place_id)
        self.assertIsNotNone(retrieved_place)

        retrieved_partner = Partner.get_from_id(comment.partner_id)
        self.assertIsNotNone(retrieved_partner)

        retrieved_parent = Comment.get_from_id(comment.parent_id)
        self.assertIsNotNone(retrieved_parent)

        # On user deletion, the comment should be anonymous
        comment = self.create_comment_with_relations()
        User.get_from_id(comment.user_id).delete()
        self.assertIsNotNone(Comment.get_from_id(comment.id))

        # On place deletion, the comment should be deleted
        comment = self.create_comment_with_relations()
        Place.get_from_id(comment.place_id).delete()
        self.assertIsNone(Comment.get_from_id(comment.id))
        
        # On partner deletion, the comment should be deleted
        comment = self.create_comment_with_relations()
        Partner.get_from_id(comment.partner_id).delete()
        self.assertIsNone(Comment.get_from_id(comment.id))
        
        # On parent deletion, the comment should be deleted
        comment = self.create_comment_with_relations()
        Comment.get_from_id(comment.parent_id).delete()
        self.assertIsNone(Comment.get_from_id(comment.id))


    def test_update(self):
        '''Tests the update in the database'''
        comment = Comment.from_dict(TEST_COMMENT)
        comment_id = comment.save()

        comment_2 = Comment.from_dict(TEST_COMMENT)
        comment_id_2 = comment_2.save()

        comment_2.content = 'My comment 2'
        comment_2.points = 1001

        comment_2.save()

        retrieved_comment = Comment.get_from_id(comment_id)
        retrieved_comment_2 = Comment.get_from_id(comment_id_2)

        self.assertNotEqual(retrieved_comment, retrieved_comment_2)


    def test_delete(self):
        '''Tests the deletion from the database'''
        comment = Comment.from_dict(TEST_COMMENT)
        comment_id = comment.save()

        comment_2 = Comment.from_dict(TEST_COMMENT)
        comment_id_2 = comment_2.save()
        comment_2.delete()

        retrieved_comment = Comment.get_from_id(comment_id)
        retrieved_comment_2 = Comment.get_from_id(comment_id_2)

        self.assertIsNotNone(retrieved_comment)
        self.assertIsNone(retrieved_comment_2)


    def tearDown(self):
        '''Finalise the test removing the test database file'''
        #self.delete_db()