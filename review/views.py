import jwt
import json

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction
from datetime     import datetime,timedelta,timezone

from user.models       import User
from review.models     import Review, JoinReviewMenu, ReviewImage
from restaurant.models import Restaurants, Menus
from order.models      import Order, JoinOrderMenu
from utils             import login_confirm

class ReviewView(View):
    @login_confirm
    #@transaction.atomic <== 함수 전부 걸림
    def post(self, request, restaurant_id):
        user                  = request.user
        review_data           = json.loads(request.body)
        restaurant_for_review = Restaurants.objects.get(id = restaurant_id)

        with transaction.atomic():
            if Order.objects.filter(
                user           = user,
                restaurant     = restaurant_for_review,
                created_at_gte = datetime.now() - datetime.now().timedelta(days = 7)
            ).exist():
                return JsonResponse({'message':'INVALID_USER'}, status = 401)

            ratings = review_data['rating']
            review  = Review(
                order           = latest_order_of_user,
                user            = user_who_wrote_review,
                restaurant      = restaurant_for_review,
                comment         = review_data['comment'],
                rating_taste    = rating['taste'],
                rating_delivery = rating['delivery'],
                rating_quantity = rating['quantity'],
                rating_avg      = sum(ratings.values()) / len(ratings),
            )
            review.save()

            menus = [JoinReviewMenu(
                        review = review,
                        menu   = Menus.objects.get(id=menu['id']),
                        amount = menu["amount"]
            ) for menu in review_data['menu']]

            JoinReviewMenu.objects.bulk_create(menus)

            images = [ReviewImage(
                review       = review,
                review_image = img,
            ) for img in data["review_img"]]
            
            ReviewImage.objects.bulk_create(images)

        return HttpResponse(status=200)

    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurants.objects.get(id = restaurant_id)
            reviews    = list(Review.objects.filter(restaurant = restaurant).order_by('-id').values())
           
            ## select related 사용 하세요
            for i in range(len(reviews_about_restaurant)):
                reviews_about_restaurant[i]['menus'] = list()
                menus_info_of_order                  = list(JoinOrderMenu.objects.filter(order_id = reviews_about_restaurant[i]['order_id']).values())
                for menu in menus_info_of_order:
                    menu_dict           = dict()
                    menu_dict['id']     = menu['menu_id']
                    menu_dict['name']   = Menus.objects.get(id=menu['menu_id']).name
                    menu_dict['amount'] = menu['amount']
                    reviews_about_restaurant[i]['menus'].append(menu_dict)
                    
            return JsonResponse(reviews_about_restaurant, status=200, safe=False)
        except Restaurants.DoesNotExist:
            return JsonResponse({'message':'RESTAURANT_NOT_EXIST'}, status=400)
