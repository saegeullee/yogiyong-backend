import jwt
import json

from django.http  import JsonResponse
from django.views import View
from datetime     import datetime

from user.models       import User
from .models           import Order, JoinOrderMenu
from restaurant.models import Restaurants, Menus, PaymentMethods

class OrderView(View):
    def post(self, request):
        order_data_header = json.loads(request.header)
        order_data        = json.loads(request.body)
        now_datetime      = datetime.now()
        try:
            #로그인한 유저
            if 'Authorization' in list(order_data_header.keys()): 
                user_token         = order_data_header['Authorization']
                order_user_payload = jwt.decode(user_token, 'secret', algorithms=['HS256'])
                order_user         = User.objects.get(id=order_user_payload['id'])
            #비로그인 유저
            else:
                order_user         = None

            order_restaurant     = Restaurants.objects.get(id=order_data['restaurant']['id'])
            order_payment_method = PaymentMethods.objects.get(id=order_Data['payment']['id'])
            """
            order_menu_ids     = list()
            order_menu_amounts = list()
            
            for dish in order_data['menu']:
                order_menu_ids.append(dish['id'])
                order_menu_amounts.append(dish['amount'])
            #여러개의 메뉴의 아이디와 양을 정리한 리스트
            """ 
            Order(
                user              = order_user,
                user_phone_number = order_data['user_phone_number'],
                order_request     = order_data['order_request'],
                restaurant        = order_restaurant,
                delivery_fee      = float(order_data['delivery_fee']),
                delivery_address  = order_data['delivery_address'],
                payment_method    = order_payment_method,
                created_at        = now_datetime,
                ).save()

            for dish in order_data['menu']:
                JoinOrderMenu(
                    order  = Order.objects.latest('created_at')
                    menu   = Menus.objects.get(id=dish['id'])
                    amount = int(dish['amount'])
                    ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)
                    
        except User.DoesNotExist:

            return JsonResponse({'message':'INVALID_USER'}, status=401)
            
        except Restaurant.DoesNotExist:
             
            return JsonResponse({'message':'INVALID_RESTAURANT'}, status=400)

        except Menus.DoesNotExist:
                
            return JsonResponse({'message':'INVALID_MENU'}, status=400)

        except PaymentMethods.DoesNotExist:

            return JsonResponse({'message':'INVALID_PAYMENT_METHOD'}, status=400)
            
        except jwt.ExpiredSignatureError:
            
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)
            
        except jwt.InvalidIssuerError:

            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except jwt.DecodeError:
            
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except KeyError:

            return JsonResponse({'message':'WRONG_KEY'},status=400)
