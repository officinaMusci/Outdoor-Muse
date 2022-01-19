import os
import unittest

from entities.user import User


class TestUser(unittest.TestCase):
    '''Tests the User object'''

    def delete_db(self):
        '''Delete test database file'''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


    def setUp(self):
        '''Initialize the test'''
        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_user.db'
        )

        self.delete_db()
        
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"


    def test_create(self):
        '''Tests the creation in the database'''
        user = User.generate_random()
        user_id = user.save()
        retrieved_user = User.get_from_id(user_id)

        self.assertEqual(user, retrieved_user)


    def test_update(self):
        '''Tests the update in the database'''
        user = User.generate_random()
        user_id = user.save()

        user_2 = User.generate_random()
        user_id_2 = user_2.save()

        user_2.email = User.generate_random().email
        user_2.password = User.generate_random().password

        user_2.save()

        retrieved_user = User.get_from_id(user_id)
        retrieved_user_2 = User.get_from_id(user_id_2)

        self.assertNotEqual(retrieved_user, retrieved_user_2)


    def test_delete(self):
        '''Tests the deletion from the database'''
        user = User.generate_random()
        user_id = user.save()

        user_2 = User.generate_random()
        user_id_2 = user_2.save()
        user_2.delete()

        retrieved_user = User.get_from_id(user_id)
        retrieved_user_2 = User.get_from_id(user_id_2)

        self.assertIsNotNone(retrieved_user)
        self.assertIsNone(retrieved_user_2)


    def test_security(self):
        '''Tests the creation and modification of the password'''
        user = User.generate_random()
        user.save()

        # Try to retrieve the user from credentials
        retrieved_user = User.get_from_credentials(
            email=user.email,
            password=user.password
        )
        self.assertIsInstance(retrieved_user, User)

        # Modify password
        old_password = user.password
        new_password = User.generate_random().password
        user.password = new_password
        user.save()

        # Try to retrieve the user with old credentials
        retrieved_user = User.get_from_credentials(
            email=user.email,
            password=old_password
        )
        self.assertIsNone(retrieved_user)

        # Try to retrieve the user with new credentials
        retrieved_user = User.get_from_credentials(
            email=user.email,
            password=new_password
        )
        self.assertIsInstance(retrieved_user, User)


    def tearDown(self):
        '''Finalise the test removing the test database file'''
        self.delete_db()