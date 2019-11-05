import jwt
import json

from django.http  import JsonResponse
from django.views import View
from datetime     import datetime,timedelta,timezone

from user.models       import User
from review.models     import Review, JoinReviewMenu, ReviewImage
from restaurant.models import Restaurants, Menus
from order.models      import Order
from utils             import LoginConfirm

#사용자가 리뷰를 남기면 DB에 저장
class ReviewRegisterView(View):
    @LoginConfirm
    def post(self, request, restaurant_id):
        user_who_wrote_review = request.user
        request_time          = datetime.now(timezone.utc) 
        review_data           = json.loads(request.body)
        restaurant_for_review = Restaurants.objects.get(id=restaurant_id)
        orders_of_user        = Order.objects.filter(user=user_who_wrote_review, restaurant=restaurant_for_review).order_by('-id')
            
        if len(orders_of_user) == 0:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        latest_order_of_user = orders_of_user[0]
        date_of_latest_order = latest_order_of_user.created_at #가장 최근 주문의 생성날짜
        #주문한지 7일이 지났다면 리뷰를 쓸수 없음
        days                 = 60*60*24
        if (request_time-date_of_latest_order).total_seconds() > (7*days):
            return JsonResponse({'message':'EXPIRED_PERIOD'}, status=401) 

        rating=review_data['rating']
        #리뷰 등록
        Review(
            order           = latest_order_of_user,
            user            = user_who_wrote_review,
            restaurant      = restaurant_for_review,
            comment         = review_data['comment'],
            rating_taste    = rating['taste'],
            rating_delivery = rating['delivery'],
            rating_quantity = rating['quantity'],
            rating_avg      = sum(rating.values()) / len(rating),
            created_at      = request_time,
            ).save()
        #방금 등록한 리뷰를 변수에 저장
        saved_review = Review.objects.latest('created_at')
        #menu와 review 연결
        join_review_menu_list = []
        for i in range(len(review_data['menus'])):
            join_review_menu_list.append(JoinReviewMenu(
                                            review = saved_review,
                                            menu   = Menus.objects.get(id=review_data['menus'][i]['id']),
                                            amount = review_data['amounts'][i],
                                            ))
        JoinReviewMenu.objects.bulk_create(join_review_menu_list)
        #review img와 review 연결 
        if len(review_data['review_img']) != 0:
            review_img_list = []
            for i in range(len(review_data['review_img'])):
                review_img_list.append(ReviewImage(
                                                review       = saved_review,
                                                review_image = review_data['review_img'][i], 
                                                ))
            ReviewImage.objects.bulk_create(review_img_list)

        return JsonResponse({'message':'SUCCESS'}, status=200)

#DB에 저장되어 있는 리뷰들을 보내주는 view
class ReviewView(View):
    def get(self, request, restaurant_id):
        requested_restaurant    = Restaurants.objects.get(id=restaurant_id)
        review_about_restaurant = list(Review.objects.filter(restaurant = requested_restaurant).order_by('-id').values())

        return JsonResponse(review_about_restaurant, status=200, safe=False)
