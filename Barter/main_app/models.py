import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
	FN = 'FN'
	BK = 'BK'
	ED = 'ED'
	DG = 'DG'
	AP = 'AP'
	AC = 'AC'
	SH = 'SH'
	ST = 'ST'
	categories = [
		(FN, 'Furniture'),
		(BK, 'Book'),
		(ED, 'Electronic Device'),
		(DG, 'Digital Good'),
		(AP, 'Apparel'),
		(SH, 'Shoes'),
		(AC, 'Accessories'),
		(ST, 'College Supply')
	]

	pid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	category = models.CharField(max_length=2, choices=categories, default=BK)
	title = models.CharField(max_length=128)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	description = models.TextField()
	date_posted = models.DateField()

	def __str__(self):
		return self.title

class Wishlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user.username}: {self.item.title}'
