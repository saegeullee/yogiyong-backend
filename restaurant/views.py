import json

from django.http import JsonResponse
from django.views import View
from .models import Restaurants, Categories, Restaurants_Categories, Tags, PaymentMethods, Menus, MenuCategories, Restaurants_Tags

class HomeView(View): 
    def get(self, request): 
        categories = Categories.objects.values() 
        return JsonResponse({"categories" : list(categories)}) 

class CategoryView(View):

    def get(self, request, category_id):

        try:
            order_method = request.GET.get('order_method', 'id')

            restaurants  = Restaurants_Categories.objects.filter(
                category_id = category_id).order_by(
                    f"-restaurant__{order_method}").select_related(
                    'restaurant').prefetch_related(
                    'restaurant__tags_set')[:1]

            restaurants_list = [
                {
                    'id' : rest.restaurant.id,
                    'name' : rest.restaurant.name,
                    'address' : rest.restaurant.address,
                    'phone' : rest.restaurant.phone,
                    'lat' : rest.restaurant.lat,
                    'lng' : rest.restaurant.lng,
                    'phone_order' : rest.restaurant.phone_order,
                    'free_delivery_threshold' : rest.restaurant.free_delivery_threshold,
                    'delivery_fee_explanation' : rest.restaurant.delivery_fee_explanation,
                    'threshold' : rest.restaurant.threshold,
                    'logo_url' : rest.restaurant.logo_url,
                    'estimated_delivery_time' : rest.restaurant.estimated_delivery_time,
                    'city' : rest.restaurant.city,
                    'review_count' : rest.restaurant.review_count,
                    'open_time_description' : rest.restaurant.open_time_description,
                    'additional_discount' : rest.restaurant.additional_discount,
                    'review_image_count' : rest.restaurant.review_image_count,
                    'is_available_pickup' : rest.restaurant.is_available_pickup,
                    'delivery_fee' : rest.restaurant.delivery_fee,
                    'review_avg' : rest.restaurant.review_avg,
                    'one_dish' : rest.restaurant.one_dish,
                    'ingredients_origin' : rest.restaurant.ingredients_origin,
                    'company_name' : rest.restaurant.company_name,
                    'company_number' : rest.restaurant.company_number,
                    'tags' : [
                        tag["name"] for tag in rest.restaurant.tags_set.values()
                    ]
                } for rest in restaurants]

        except Restaurants_Categories.DoesNotExist:
            return JsonResponse({"RESULT" : "NO_RESTAURANT_CATEGORY"})
        
        return JsonResponse({"restaurants" : restaurants_list, "restaurants_number" : len(restaurants_list)}, status=200)

class RestaurantView(View):
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurants.objects.values().get(id=restaurant_id)
            payment_methods = PaymentMethods.objects.values().filter(restaurant_id=restaurant_id)
            menu_categories = MenuCategories.objects.values().filter(restaurant_id=restaurant_id)
        except Restaurants.DoesNotExist:
            return JsonResponse({"RESULT" : "NO_RESTAURANT"})
        except PaymentMethods.DoesNotExist:
            return JsonResponse({"RESULT" : "NO_PAYMENTMETHOD"})
        except MenuCategories.DoesNotExist:
            return JsonResponse({"RESULT" : "NO_MENUCATEGORY"})

        paymentmethods = []
        for payment_method in payment_methods:
            paymentmethods.append(payment_method["name"])

        all_menus = [
            {
                "title" : menu_category["name"],
                "menus" : [
                    menuItem 
                    for menuItem in Menus.objects.values().filter(menu_category_id=menu_category['id'])]
            }
            for menu_category in menu_categories]

        return JsonResponse({"restaurant" : restaurant, "all_menus" : all_menus, "payment_methods" : paymentmethods})
        

         