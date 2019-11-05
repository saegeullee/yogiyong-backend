import jwt
import json

from django.http  import JsonResponse
from django.views import View
from datetime     import datetime, timezone

from user.models       import User
from .models           import Order, JoinOrderMenu
from restaurant.models import Restaurants, Menus, PaymentMethods
from utils             import OrderLoginConfirm

class OrderView(View):
    @OrderLoginConfirm
    def post(self, request):
        try:
            order_data           = json.loads(request.body)
            now_datetime         = datetime.now(timezone.utc) #DB에 저장할 때는 국제표준으로 저장
            order_user           = request.user
            order_restaurant     = Restaurants.objects.get(id=order_data['restaurant']['id'])
            order_payment_method = PaymentMethods.objects.get(id=order_data['payment_method']['id'])
           
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

            menu_list   = order_data['menus']
            amount_list = order_data['amounts']
            
            join_order_menu =[]
            for i in range(len(menu_list)):
                join_order_menu.append(JoinOrderMenu(
                                                order  = Order.objects.latest('created_at'),
                                                menu   = Menus.objects.get(id=menu_list[i]['id']),
                                                amount = amount_list[i],
                                                ))
            JoinOrderMenu.objects.bulk_create(join_order_menu)

            return JsonResponse({'message':'SUCCESS'}, status=200)
                    
        except Restaurants.DoesNotExist:
            return JsonResponse({'message':'INVALID_RESTAURANT'}, status=400)

        except Menus.DoesNotExist:
            return JsonResponse({'message':'INVALID_MENU'}, status=400)

        except PaymentMethods.DoesNotExist:
            return JsonResponse({'message':'INVALID_PAYMENT_METHOD'}, status=400)
            
        except KeyError:
            return JsonResponse({'message':'WRONG_KEY'}, status=400)
