from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Item
from .forms import LoginForm, RegisterForm, ListingForm
import uuid

# Create your tests here.

OK = 200
FOUND = 302
NOT_FOUND = 404

VALID_USERNAME = 'testuser'
VALID_PASSWORD = '123123'
VALID_ITEM_PID = uuid.uuid1()
VALID_USERNAME2 = 'testuser2'
VALID_ITEM_PID2 = uuid.uuid1()

class UnitTester(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client = Client()
        user = User.objects.get_or_create(username=VALID_USERNAME, email='test@sjsu.edu', first_name='test', last_name='user')[0]
        user.set_password(VALID_PASSWORD)
        user.save()
        user2 = User.objects.get_or_create(username=VALID_USERNAME2, email='test2@sjsu.edu', first_name='test', last_name='user')[0]
        user2.set_password(VALID_PASSWORD)
        user2.save()
        user2.save()

        Item.objects.get_or_create(user=user, pid=VALID_ITEM_PID, category='ST', title="test item", date_posted="2020-01-01", description="test description", price="100")
        Item.objects.get_or_create(user=user2, pid=VALID_ITEM_PID2, category='ST', title="test item", date_posted="2020-01-01", description="test description", price="100")

    def test_create_post(self):
        response = self.client.get('/createlisting');
        self.assertRedirects(response, "http://localhost:8000/login", fetch_redirect_response = False)				#Attempt to enter page without login
        

        list_data = {'title':'test', 'category':'FN', 'price':'1', 'description':'test'}
        listing_form = ListingForm(list_data)
        self.assertTrue(listing_form.is_valid()) #correct case

        list_data['title'] = ''
        listing_form = ListingForm(list_data)
        self.assertTrue(not listing_form.is_valid()) #no title

        list_data['price'] = 'letters'
        listing_form = ListingForm(list_data)
        self.assertTrue(not listing_form.is_valid()) #letters in price

        list_data['price'] = '-1'
        listing_form = ListingForm(list_data)
        self.assertTrue(not listing_form.is_valid()) #negative number in price

        list_data['description'] = ''
        listing_form = ListingForm(list_data)
        self.assertTrue(not listing_form.is_valid()) #no description
    def test_login(self):
        form_data = {'username': VALID_USERNAME, 'password':''}     # empty password
        login_form = LoginForm(data=form_data)
        self.assertTrue(not login_form.is_valid())
        form_data['password'] = "12312"                             # Invalid Password
        login_form = LoginForm(data=form_data)
        self.assertTrue(not login_form.is_valid())
        form_data['password'] = "123123"                            # Valid Password
        login_form = LoginForm(data=form_data)
        self.assertTrue(login_form.is_valid())

    def test_register_user(self):
        form_data = {'username':'testuser', 'email':'test@sjsu.edu', 'name':'test user', 'password':'123123', 'confirm_password':'12312'}
        reg_form = RegisterForm(data=form_data)                     # Duplicate username
        self.assertTrue(not reg_form.is_valid())

        form_data['username'] = 'testuser2'                         # New user name, but same email
        reg_form = RegisterForm(data=form_data)
        self.assertTrue(not reg_form.is_valid())

        form_data['email'] = 'testuser2@sjsu.edu'                   # New user name, new email, passwords do not match
        reg_form = RegisterForm(data=form_data)
        self.assertTrue(not reg_form.is_valid())

        form_data['confirm_password'] = '123123'                    # Everything is correct now.
        reg_form = RegisterForm(data=form_data)
        self.assertTrue(reg_form.is_valid())

        form_data['email'] = 'testuser2@gmail.com'                  # Using non sjsu email address
        reg_form = RegisterForm(data=form_data)
        self.assertTrue(not reg_form.is_valid())


    def test_update_post(self):
        response = self.client.post('/login', {'username': VALID_USERNAME, 'password': VALID_PASSWORD, 'login' : 'true'})
        response = self.client.post(f'/update_listing/{VALID_ITEM_PID}', 
        {
            'title': 123,
            'category': 'ST',
            'price': 123,
            'description': 123
        })
        self.assertEqual(response.status_code, OK)

    def test_delete_post(self):
        response = self.client.post('/login', {'username': VALID_USERNAME, 'password': VALID_PASSWORD, 'login' : 'true'})
        response = self.client.get(f'/delete_listing/{VALID_ITEM_PID}')
        response = self.client.get(f'/listing/{VALID_ITEM_PID}')
        self.assertEqual(response.status_code, NOT_FOUND)

    def test_delete_other_user_post(self):
        response = self.client.post('/login', {'username': VALID_USERNAME, 'password': VALID_PASSWORD, 'login' : 'true'})
        response = self.client.get(f'/delete_listing/{VALID_ITEM_PID2}')
        response = self.client.get(f'/listing/{VALID_ITEM_PID2}')
        self.assertEqual(response.status_code, OK)
