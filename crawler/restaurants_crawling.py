import requests

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yogiyong.settings")
import django
django.setup()

from restaurant.models import Restaurants, Tags, PaymentMethods, Categories, Menus, MenuCategories, Restaurants_Categories, Restaurants_Tags

categories = ["1인분주문", "프랜차이즈", "치킨", "피자양식", "중식", "한식", "일식돈까스", "족발보쌈", "야식",
            "분식", "카페디저트", "편의점"]

def getRestaurantUrl(pageNum):
    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/?items=20&lat=37.5030428702997&lng=127.050691968657&order=rank&page={pageNum}&search="
    return url

def getRestaurantInfoUrl(restaurant_id):
    url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{restaurant_id}/info/"
    return url

def getMenuUrl(restaurant_id):
    url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{restaurant_id}/menu/?add_photo_menu=android&add_one_dish_menu=true"
    return url

headers = {'x-apikey': 'iphoneap', 'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'}

def saveAllRestaurantsAppModelsData(categories):
    for i in range(50):
        req = requests.get(getRestaurantUrl(i), headers=headers)
        restaurants_obj = req.json()["restaurants"]

        for rest_obj in restaurants_obj:

            info_req = requests.get(getRestaurantInfoUrl(rest_obj["id"]), headers=headers)
            info_obj = info_req.json()

            restaurant = Restaurants(
                name = rest_obj["name"],
                address = rest_obj["address"],
                phone = rest_obj["phone"],
                lat = rest_obj["lat"],
                lng = rest_obj["lng"],
                phone_order = rest_obj["phone_order"],
                free_delivery_threshold = rest_obj["free_delivery_threshold"],
                delivery_fee_explanation = rest_obj["delivery_fee_explanation"],
                threshold = rest_obj["threshold"],
                logo_url = rest_obj["logo_url"],
                estimated_delivery_time = rest_obj["estimated_delivery_time"],
                city = rest_obj["city"],
                review_count = rest_obj["review_count"],
                open_time_description = rest_obj["open_time_description"],
                additional_discount = rest_obj["additional_discount"],
                review_image_count = rest_obj["review_image_count"],
                is_available_pickup = rest_obj["is_available_pickup"],
                delivery_fee = rest_obj["delivery_fee"],
                review_avg = rest_obj["review_avg"],
                one_dish = rest_obj["one_dish"],
                ingredients_origin = info_obj["country_origin"],
                company_name = info_obj["crmdata"]["company_name"],
                company_number = info_obj["crmdata"]["company_number"]
            )

            restaurant.save()
            print(rest_obj["name"] + "restaurants saved")

            categories_obj = rest_obj["categories"]
            
            for cat_obj in categories_obj: 
                try:
                    category = Categories.objects.get(name=cat_obj)
                    Restaurants_Categories(
                        category = category,
                        restaurant = restaurant
                    ).save()
                except Categories.DoesNotExist:
                    pass
            print("category saved")

            tags_obj = rest_obj["tags"]
            for tag_obj in tags_obj:
                
                tag = Tags.objects.get(name=tag_obj)
                Restaurants_Tags(
                    tag = tag,
                    restaurant = restaurant
                ).save()
            print("tags saved")

            payment_methods_obj = rest_obj["payment_methods"]

            payment_object = [
                PaymentMethods(
                    restaurant = restaurant,
                    name = payment_method)
                for payment_method in payment_methods_obj
            ]
            PaymentMethods.objects.bulk_create(payment_object)

            print("payment_method saved")
            saveAllRestaurantsMenus(rest_obj["id"], restaurant)
    print("CATEGORY saved")
                

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

