from django.db import models
'''
python manage.py makemigrations flow
python manage.py migrate flow

'''
# Create your models here.
class UserData(models.Model):
	lms_id = models.CharField(max_length = 50)
	device_token = models.CharField(max_length = 200, default = 'null')
	old_subjects = models.CharField(max_length = 200, default = 'null')
	old_reports = models.CharField(max_length = 500, default = 'null')
	recent_push = models.CharField(max_length = 300, default = '[]')
	def __str__(self):
		return self.lms_id