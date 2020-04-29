from django.test import TestCase
from django.test import Client

# Create your tests here.

OK = 200
FOUND = 302

VALID_USERNAME = 'cheryltownsend'
VALID_PASSWORD = 'pwdcheryltownsend1234'
VALID_ITEM_PID = 'pwdcheryltownsend1234'

class UnitTester(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client = Client()

    def test_update_post(self):
        response = self.client.post('/login', {'username': VALID_USERNAME, 'password': VALID_PASSWORD})
        response2 = self.client.get('update_listing/%3FPd037d5fc-89b4-11ea-960e-3af9d372bd52%5Cw+')
        response3 = self.client.post('update_listing/%3FPd037d5fc-89b4-11ea-960e-3af9d372bd52%5Cw+', 
        {
            'title': 123,
            'category': 'ST',
            'price': 123,
            'description': 123
        })
        self.assertEqual(response.status_code, OK)

    def test_delete_post(self):
        response = self.client.post('/login', {'username': 'cheryltownsend', 'password': 'pwdcheryltownsend1234'})
        response2 = self.client.get('delete_listing/%3FPd037d5fc-89b4-11ea-960e-3af9d372bd52%5Cw+')
        self.assertEqual(response.status_code, OK)

    

