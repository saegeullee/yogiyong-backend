import json

from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from .models import (
    Restaurants,
    Categories, 
    RestaurantsCategories,
    Tags,
    PaymentMethods,
    Menus,
    MenuCategories,
    Restaurants_Tags
)

class CategoryListView(View): 
    def get(self, request): 
        categories = Categories.objects.values() 

        return JsonResponse({"categories" : list(categories)}) 

class CategoryView(View):
    def get(self, request, category_id):
        try:
            order_method = request.GET.get('order_method', 'id')
            limit        = int(request.GET.get('limit', 20))
            offset       = int(request.GET.get('offset', 0))
            
            restaurants_count = RestaurantsCategories.objects.filter(category_id = category_id).count()
            order_by    = f"-restaurant__{order_method}"
            restaurants = (
                RestaurantsCategories.objects.
                    filter(category_id = category_id).
                    order_by(order_by).
                    select_related('restaurant').
                    prefetch_related('restaurant__tags_set')[offset:limit]
            )

            restaurants_list = [
                {
                    'id'                       : rest.restaurant.id,
                    'name'                     : rest.restaurant.name,
                    'address'                  : rest.restaurant.address,
                    'phone'                    : rest.restaurant.phone,
                    'lat'                      : rest.restaurant.lat,
                    'lng'                      : rest.restaurant.lng,
                    'phone_order'              : rest.restaurant.phone_order,
                    'free_delivery_threshold'  : rest.restaurant.free_delivery_threshold,
                    'delivery_fee_explanation' : rest.restaurant.delivery_fee_explanation,
                    'threshold'                : rest.restaurant.threshold,
                    'logo_url'                 : rest.restaurant.logo_url,
                    'estimated_delivery_time'  : rest.restaurant.estimated_delivery_time,
                    'city'                     : rest.restaurant.city,
                    'review_count'             : rest.restaurant.review_count,
                    'open_time_description'    : rest.restaurant.open_time_description,
                    'additional_discount'      : rest.restaurant.additional_discount,
                    'review_image_count'       : rest.restaurant.review_image_count,
                    'is_available_pickup'      : rest.restaurant.is_available_pickup,
                    'delivery_fee'             : rest.restaurant.delivery_fee,
                    'review_avg'               : rest.restaurant.review_avg,
                    'one_dish'                 : rest.restaurant.one_dish,
                    'ingredients_origin'       : rest.restaurant.ingredients_origin,
                    'company_name'             : rest.restaurant.company_name,
                    'company_number'           : rest.restaurant.company_number,
                    'tags' : [
                        tag["name"] for tag in rest.restaurant.tags_set.values()
                    ]
                } for rest in restaurants]

            return JsonResponse({
                "restaurants" : restaurants_list,
                "total_count" : restaurants_count
            }, status=200)
        except RestaurantsCategories.DoesNotExist:
            return JsonResponse({"RESULT" : "NO_RESTAURANT_CATEGORY"}, status=400)

class RestaurantView(View):
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurants.objects.values().get(id=restaurant_id)

            result = {
                "name" : restaurant.name,
                ....,
                "menus"  : restaurant.menus.values(),
                "payment_methods" : restaurant.payment_methods.values()
            }

            return JsonResponse({"restaurant" : result}, status=200)
        except Restaurants.DoesNotExist
            return JsonResponse({"RESULT" : "NO_RESTAURANT"}, status=400)
       
class RestaurantsSearchView(View):
    def get(self, request):
        try:
            query  = request.GET.get("query", "")
            limit  = request.GET.get("limit", 20)
            offset = request.GET.get("offset", 0)

            if query == "":
                return JsonResponse({"RESULT" : "INVALID_QUERY"}, status=400)

            total_count = Restaurants.objects.filter(name__icontains=query).count()
            restaurants = Restaurants.objects.filter(name__icontains=query)[offset:limit].values()

            return JsonResponse({
                "restaurants" : list(restaurants),
                "total_count" : total_count
            }, status=200)
        except Restaurants.DoesNotExist:
            return JsonResponse({"RESULT" : "RESTAURANT_DOES_NOT_EXIST"}, status=400)
