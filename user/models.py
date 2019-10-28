from django.db import models

class SocialPlatforms(models.Model):
	platform_name=models.CharField(max_length=20)
 
class Users(models.Model):
	email=models.CharField(max_length=200, unique=True)
	password=models.CharField(max_length=500)
	nickname=models.CharField(max_length=400, null=True)
	joined_platform=models.ForeignKey(SocialPlatforms, on_delete=models.SET_NULL, null=True)
	class Meta:
		db_table='users_list'
