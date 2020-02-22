import uuid
from django.db import models

# Create your models here.
class Post(models.Model):
	pid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=128)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	description = models.TextField()
	date_posted = models.DateField()

	def __str__(self):
		return self.title
