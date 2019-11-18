from django.db import models

class SocialPlatform(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'social_platforms'

class User(models.Model):
    email                  = models.CharField(max_length=70, unique=True)
    password               = models.CharField(max_length=400)
    notification_accept    = models.BooleanField(default=False)
    nickname               = models.CharField(max_length=50, blank=True)
    phone_number           = models.CharField(max_length=11, null=True)
    #social_platform        = models.ForeignKey(SocialPlatform, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'users'

class AuthCode(models.Model):
    phone_number = models.CharField(max_length=11)
    auth_number  = models.IntegerField()
    created_at   = models.DateTimeField()

    class Meta:
        db_table = 'auth_numbers'
