from django.db import models

# Create your models here.

class Person(models.Model):
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)

class Test(models.Model):
	ID = models.CharField(max_length = 30)
	PW = models.CharField(max_length = 30)