import jwt
import json
from django.http  import JsonResponse
from django.views import View

from review.models     import Review
from restaurant.models import Restaurant

"""
#사용자가 리뷰를 남기면 DB에 저장
class ReviewRegisterView(View):
    def post(self, request):
        try:
            review_data_header = json.loads(request.header)
            if 'Authorization' in list(review_data_header.keys()):
                user_token         = review_data_header['Authorization']
                user_token_payload = jwt.decode(user_token, 'secret', algorithms=['HS256'])
            else:
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            review_data = json.loads(request.body)
            user_id     = user_token_payload['id']
            
        except jwt.ExpiredSignatureError:
 
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)
 
        except jwt.InvalidIssuerError:
 
            return JsonResponse({'message':'INVALID_USER'}, status=401)
 
        except jwt.DecodeError:
 
            return JsonResponse({'message':'INVALID_USER'}, status=401)
"""
#DB에 저장되어 있는 리뷰들을 보내주는 view
class ReviewView(View):
    def get(self, request, restaurant_id):
        #어느 음식점의 리뷰인가
        #식당의 아이디를 알면
        #그 식당의 아이디를 포함하고 있는 리뷰들을
        #최신부터 쭉 나열한다.
        requested_restaurant=Restaurant.objects.get(id=restaurant_id)
        review_about_restaurant = list(Review.objects.filter(restaurant = requested_restaurant).values())
        return JsonResponse(review_about_restaurant, status=200)
        
