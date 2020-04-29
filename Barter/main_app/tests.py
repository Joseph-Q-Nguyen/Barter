from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Item
import uuid

# Create your tests here.

OK = 200
FOUND = 302

VALID_USERNAME = 'testuser'
VALID_PASSWORD = '123123'
VALID_ITEM_PID = uuid.uuid1()

class UnitTester(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client = Client()
        user = User.objects.get_or_create(username=VALID_USERNAME, email='test@sjsu.edu', first_name='test', last_name='user')[0]
        user.set_password(VALID_PASSWORD)
        user.save()
        Item.objects.get_or_create(user=user, pid=VALID_ITEM_PID, category='ST', title="test item", date_posted="2020-01-01", description="test description", price="100")

    def test_update_post(self):
        response = self.client.post('/login', {'username': VALID_USERNAME, 'password': VALID_PASSWORD})
        response2 = self.client.get(f'update_listing/{VALID_ITEM_PID}')
        response3 = self.client.post(f'update_listing/{VALID_ITEM_PID}', 
        {
            'title': 123,
            'category': 'ST',
            'price': 123,
            'description': 123
        })
        self.assertEqual(response.status_code, OK)

    def test_delete_post(self):
        response = self.client.post('/login', {'username': VALID_USERNAME, 'password': VALID_PASSWORD})
        response2 = self.client.get(f'delete_listing/{VALID_ITEM_PID}')
        self.assertEqual(response.status_code, OK)


    

