import requests

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yogiyong.settings")
import django
django.setup()

from restaurant.models import Restaurants, Tags, PaymentMethods, Categories, Menus, MenuCategories, Restaurants_Categories, Restaurants_Tags

categories = ["1인분 주문", "프랜차이즈", "치킨", "피자/양식", "중국집", "한식", "일식/돈까스", "족발/보쌈", "야식",
            "분식", "카페/디저트", "편의점"]

def getCategoryUrl(categoryName):
    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/?category={categoryName}&items=20&lat=37.5342877292787&lng=126.965315612204&order=rank&page=0&search="
    return url

def getMenuUrl(restaurant_id):
    url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{restaurant_id}/menu/?add_photo_menu=android&add_one_dish_menu=true"
    return url

headers = {'x-apikey': 'iphoneap', 'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'}

def saveAllRestaurantsAppModelsData(categories):
    for category_idx in range(len(categories)):
        req = requests.get(getCategoryUrl(categories[category_idx]), headers=headers) 

        restaurants_obj = req.json()["restaurants"]

        for rest_idx in range(len(restaurants_obj)):

            obj = restaurants_obj[rest_idx]

            restaurant = Restaurants(
                name = obj["name"],
                address = obj["address"],
                phone = obj["phone"],
                lat = obj["lat"],
                lng = obj["lng"],
                phone_order = obj["phone_order"],
                free_delivery_threshold = obj["free_delivery_threshold"],
                delivery_fee_explanation = obj["delivery_fee_explanation"],
                threshold = obj["threshold"],
                logo_url = obj["logo_url"],
                estimated_delivery_time = obj["estimated_delivery_time"],
                city = obj["city"],
                review_count = obj["review_count"],
                open_time_description = obj["open_time_description"],
                additional_discount = obj["additional_discount"],
                review_image_count = obj["review_image_count"],
                is_available_pickup = obj["is_available_pickup"],
                delivery_fee = obj["delivery_fee"],
                review_avg = obj["review_avg"],
                one_dish = obj["one_dish"]
            )

            restaurant.save()
            print(obj["name"] + "restaurants saved")

            categories_obj = obj["categories"]
            for cat_idx in range(len(categories_obj)): 
                
                try:
                    category = Categories.objects.get(name=categories_obj[cat_idx])
                    Restaurants_Categories(
                        category = category,
                        restaurant = restaurant
                    ).save()
                except Categories.DoesNotExist:
                    pass
            print("category saved")

            tags_obj = obj["tags"]
            for tag_idx in range(len(tags_obj)):
                
                tag = Tags.objects.get(name=tags_obj[tag_idx])
                Restaurants_Tags(
                    tag = tag,
                    restaurant = restaurant
                ).save()
            print("tags saved")

            payment_methods_obj = obj["payment_methods"]
            for payment_idx in range(len(payment_methods_obj)):

                PaymentMethods(
                    restaurant = restaurant,
                    name = payment_methods_obj[payment_idx]
                ).save()
            print("payment_method saved")
            saveAllRestaurantsMenus(obj["id"], restaurant)
        print(categories[category_idx] + "category saved")
                

def saveAllRestaurantsMenus(restaurant_id, restaurant):
    req = requests.get(getMenuUrl(int(restaurant_id)), headers=headers)

    menuTotalListLength = len(req.json())

    for menu_cat_idx in range(menuTotalListLength):

        menuCategoryLength = len(req.json()[menu_cat_idx]['items'])

        menu_category_name = req.json()[menu_cat_idx]['name']
        menu_category = MenuCategories(
            restaurant = restaurant,
            name = menu_category_name
        )

        menu_category.save()
        print("menu category saved")

        for menu_idx in range(menuCategoryLength):

            menu = req.json()[menu_cat_idx]['items'][menu_idx]

            try:
                image = menu['image']
            except KeyError:
                image = None

            Menus(
                restaurant = restaurant,
                menu_category = menu_category,
                name = menu['name'],
                description = menu['description'],
                price = menu['price'],
                quantity = 10,
                image = image
            ).save()
        print(menu_category_name + "menus saved")
    print("All menus in the category saved")


saveAllRestaurantsAppModelsData(categories)

