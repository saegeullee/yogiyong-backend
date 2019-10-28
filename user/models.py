from django.db import models
 
class Users(models.Model):
	email=models.CharField(max_length=200, unique=True)
	password=models.CharField(max_length=500)
	nickname=models.CharField(max_length=400, null=True)
	class Meta:
		db_table='users_list'
