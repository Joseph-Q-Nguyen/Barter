import os
import random
import uuid
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Barter.settings')

import django
django.setup()

import random
from main_app.models import Item, Wishlist
from django.contrib.auth.models import User
from faker import Faker

categories = Item.categories

fk = Faker()
choose = [True, False]

def add_item(user):
	cat = random.choice(categories)
	pid = uuid.uuid1()
	title = fk.sentence()
	date_posted = fk.date()
	description = f'{fk.text()} {fk.text()}'
	price = random.randint(5, 1000)

	item = Item.objects.get_or_create(user=user, pid=pid, category=cat, title=title, date_posted=date_posted, description=description, price=price)[0]
	item.save()
	return item

def populate(N=5):
	with open("login_details.txt", 'w') as outfile:
		for i in range(N):
			name = fk.name()
			n = name.split()
			uname = ''.join(name.lower().split(' '))
			pwd = f'pwd{uname}1234'
			outfile.write(f'{uname}\t\t{pwd}\n')

			email = f'{uname}@{fk.domain_name()}'
			user = User.objects.get_or_create(username=uname, email=email, first_name=n[0], last_name=n[1])[0]
			user.set_password(pwd)
			user.save()
			item = add_item(user)
			if random.choice(choose):
				Wishlist.objects.create(item=item, user=user)
		

if __name__ == '__main__':
	print("Populating....")
	populate(50)
	print("Done populating.")

