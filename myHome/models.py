from django.db import models

# Create your models here.
class NEWS_BROADCAST(models.Model):
	id = models.IntegerField(primary_key=True)
	category = models.CharField(max_length=10)
	title = models.TextField(max_length=100)
	content = models.TextField()
	uploadDate = models.CharField(max_length=10)
	updateDate = models.DateTimeField()