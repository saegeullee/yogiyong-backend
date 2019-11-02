import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yogiyong.settings")
import django
django.setup()

from restaurant.models import Categories, Tags

categories = ["1인분 주문", "프랜차이즈", "치킨", "피자/양식", "중국집", "한식", "일식/돈까스", "족발/보쌈", "야식",
            "분식", "카페/디저트", "편의점"]

# tags = ["CESCO", "relayo", "excellent"]

def saveCategories(categories):
    for i in range(len(categories)):
        Categories(
            name = categories[i]
        ).save()

saveCategories(categories)
