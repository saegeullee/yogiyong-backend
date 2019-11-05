import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yogiyong.settings")
import django
django.setup()

from restaurant.models import Categories, Tags

categories = ["1인분주문", "프랜차이즈", "치킨", "피자양식", "중식", "한식", "일식돈까스", "족발보쌈", "야식",
            "분식", "카페디저트", "편의점"]

# tags = ["CESCO", "relayo", "excellent"]

def saveCategories(categories):
    for i in range(len(categories)):
        Categories(
            name = categories[i]
        ).save()

saveCategories(categories)
