import jwt
import json
from django.http  import JsonResponse
from django.views import View
from datetime     import datetime,timedelta,timezone

from user.models       import User
from review.models     import Review, JoinReviewMenu, ReviewImage
from restaurant.models import Restaurants, Menus
from order.models      import Order

#사용자가 리뷰를 남기면 DB에 저장
class ReviewRegisterView(View):
    def post(self, request, restaurant_id):
            #header에서 유저정보 읽기
        """
            review_data_header = json.loads(request.header)
            
            if 'Authorization' in list(review_data_header.keys()):
                user_token         = review_data_header['Authorization']
                user_token_payload = jwt.decode(user_token, 'secret', algorithms=['HS256'])
            else:
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            
            user_id               = user_token_payload['id']
            user_who_wrote_review = User.objects.get(id=user_id)
            
        """
        #유저가 없다고 가정하고 리뷰 포스팅 로직짜기
        user_who_wrote_review = None
        request_time          = datetime.now(timezone.utc)
            
        review_data           = json.loads(request.body)
            
            #restaurant_id         = review_data['restaurant']['id']
        restaurant_for_review = Restaurants.objects.get(id=restaurant_id)
             
        order_of_user         = Order.objects.filter(user=user_who_wrote_review, restaurant=restaurant_for_review).order_by('-id')
            
        if not order_of_user: #유저가 해당 식당에서 주문한적이 없는 경우
            
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        else: #유저가 해당 식당에서 주문한 적이 있는 경우
            days                 = 60*60*24
            latest_order_of_user = order_of_user[0]
            date_of_latest_order = latest_order_of_user.created_at #가장 최근 주문의 생성날짜
                
                #주문한지 7일이 지났다면 리뷰를 쓸수 없음
            if (request_time-date_of_latest_order).total_seconds() > (7*days):

                return JsonResponse({'message':'EXPIRED_PERIOD'}, status=401)
                
            else:
                rating=review_data['rating']

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
                    
                saved_review = Review.objects.latest('created_at')
                    
                for i in range(len(review_data['menus'])):
                    JoinReviewMenu(
                                review = saved_review,
                                menu   = Menus.objects.get(id=review_data['menus'][i]['id']),
                                amount = review_data['amounts'][i],
                                ).save()

                if review_data['review_img']:
                    for i in range(len(review_data['review_img'])):
                        ReviewImage(
                                review       = saved_review,
                                review_image = review_data['review_img'][i], 
                                ).save()

                    return JsonResponse({'message':'SUCCESS'}, status=200)
#DB에 저장되어 있는 리뷰들을 보내주는 view
class ReviewView(View):
    def get(self, request, restaurant_id):
        requested_restaurant    = Restaurants.objects.get(id=restaurant_id)
        review_about_restaurant = list(Review.objects.filter(restaurant = requested_restaurant).values())

        return JsonResponse(review_about_restaurant, status=200, safe=False)
"""
        except jwt.ExpiredSignatureError:
 
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)
 
        except jwt.InvalidIssuerError:
 
            return JsonResponse({'message':'INVALID_USER'}, status=401)
 
        except jwt.DecodeError:
            
            return JsonResponse({'message':'INVALID_USER'}, status=401)
"""
