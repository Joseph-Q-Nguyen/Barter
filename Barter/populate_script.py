import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Barter.settings')

import django
django.setup()

import random
from main_app.models import Post
from faker import Faker

fk = Faker()

def populate(N=5):
	for i in range(N):
		pid = i
		title = fk.sentence()
		date_posted = fk.date()
		description = f'{fk.text()} {fk.text()}'
		price = random.randint(5, 1000000)

		fwp = Post.objects.get_or_create(pid=pid, title=title, date_posted=date_posted, description=description, price=price)[0]

if __name__ == '__main__':
	print("Populating....")
	populate(50)
	print("Done populating.")

