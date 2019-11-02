from django.http import JsonResponse
from django.views import View
from .models import Restaurants, Categories, Restaurants_Categories, Tags, PaymentMethods, Menus, MenuCategories, Restaurants_Tags

import json


class HomeView(View): 
    def get(self, request): 
        categories = Categories.objects.values() 
        return JsonResponse({"categories" : list(categories)}) 

class CategoryView(View): 
    def get(self, request, category_id):
        restaurants = Restaurants_Categories.objects.values().filter(category_id=category_id)
        restaurants_list = []

        for restaurant in restaurants:
            restaurants_obj = {}
            rest = Restaurants.objects.values().get(id=restaurant["restaurant_id"])

            restaurants_obj['id'] = rest['id']
            restaurants_obj['name'] = rest['name']
            restaurants_obj['address'] = rest['address']
            restaurants_obj['phone'] = rest['phone']
            restaurants_obj['lat'] = rest['lat']
            restaurants_obj['lng'] = rest['lng']
            restaurants_obj['phone_order'] = rest['phone_order']
            restaurants_obj['free_delivery_threshold'] = rest['free_delivery_threshold']
            restaurants_obj['delivery_fee_explanation'] = rest['delivery_fee_explanation']
            restaurants_obj['threshold'] = rest['threshold']
            restaurants_obj['logo_url'] = rest['logo_url']
            restaurants_obj['estimated_delivery_time'] = rest['estimated_delivery_time']
            restaurants_obj['city'] = rest['city']
            restaurants_obj['review_count'] = rest['review_count']
            restaurants_obj['open_time_description'] = rest['open_time_description']
            restaurants_obj['additional_discount'] = rest['additional_discount']
            restaurants_obj['review_image_count'] = rest['review_image_count']
            restaurants_obj['is_available_pickup'] = rest['is_available_pickup']
            restaurants_obj['delivery_fee'] = rest['delivery_fee']
            restaurants_obj['review_avg'] = rest['review_avg']
            restaurants_obj['one_dish'] = rest['one_dish']
            
            tags_list = []
            tags = Restaurants_Tags.objects.values().filter(restaurant_id = restaurant["restaurant_id"])
            for tag in tags:
                tag_name = Tags.objects.values().get(id=tag['tag_id'])['name']
                tags_list.append(tag_name)
            
            restaurants_obj['tags'] = tags_list
            restaurants_list.append(restaurants_obj)
        
        return JsonResponse({"restaurants" : restaurants_list, "restaurants_number" : len(restaurants_list)})

class RestaurantView(View):
    def get(self, request, restaurant_id):
        restaurant = Restaurants.objects.values().get(id=restaurant_id)
        payment_methods = PaymentMethods.objects.values().filter(restaurant_id=restaurant_id)
        menu_categories = MenuCategories.objects.values().filter(restaurant_id=restaurant_id)

        paymentmethods = []
        for payment_method in payment_methods:
            paymentmethods.append(payment_method["name"])

        menus = {}
        for menu_category in menu_categories:
            menu_items = []
            menuItems = Menus.objects.values().filter(menu_category_id=menu_category['id'])
            for menuItem in menuItems:
                menu_items.append(menuItem)
            menus[menu_category["name"]] = menu_items

        return JsonResponse({"restaurant" : restaurant, "menus" : menus, "payment_methods" : paymentmethods})
        

         