from django.db import models

class SocialPlatforms(models.Model):
	platform_name=models.CharField(max_length=20)
	user=models.ManyToManyField('Users')
	
	class Meta:
		db_table='SocialPlatforms'

class Users(models.Model):
	email=models.CharField(max_length=200, unique=True, null=False)
	password=models.CharField(max_length=400)
	email_accept=models.BooleanField(default=False)
	nickname=models.CharField(max_length=50, blank=True)
	phone_number=models.CharField(max_length=100, blank=True)
	
	class Meta:
		db_table='users_list'
