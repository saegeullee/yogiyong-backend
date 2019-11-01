from django.db import models

class SocialPlatform(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'social_platforms'

class User(models.Model):
    email           = models.CharField(max_length=70, unique=True)
    password        = models.CharField(max_length=400)
    email_accept    = models.BooleanField(default=False)
    nickname        = models.CharField(max_length=50, blank=True)
    social_platform = models.ForeignKey(SocialPlatform, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'users'
