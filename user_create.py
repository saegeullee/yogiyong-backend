import requests
 
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yogiyong.settings")
import django
django.setup()

from user.models import SocialPlatform, User

social_platforms=['kakao', 'naver']

for social in social_platforms:
    SocialPlatform(
        name=social
    ).save()
