import jwt
import json
import bcrypt
import requests

from datetime          import datetime, timedelta, timezone
from random            import randint
from django.http       import JsonResponse
from django.views      import View
from .models           import User, AuthSms
from yogiyong.settings import SECRET_KEY, SMS_ACCESS_KEY_ID, SMS_URL, SMS_SERVICE_SECRET, SMS_MY_PHONE_NUMBER
from utils             import LoginConfirm
from order.models      import Order, JoinOrderMenu
from restaurant.models import Restaurants, Menus

class SignUpView(View):
    def post(self, request):
        input_data=json.loads(request.body)
        try:
            if input_data['authorized_phone_number']:
                if User.objects.filter(email=input_data['email']).exists():	
                    return JsonResponse({'message':'USER_EXISTS'}, status=409)
                
                encoded_password = input_data['password'].encode('utf-8')
                hashed_password  = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                
                User(
                    email               = input_data['email'],
                    password            = hashed_password.decode('utf-8'), #CharField이기 때문에 unicode로
                    nickname            = input_data['nickname'],
                    notification_accept = input_data['notification_accept'],
                    phone_number        = input_data['authorized_phone_number'],
                    ).save()
                        
                return JsonResponse({'message':'SUCCESS'}, status=200)

            return JsonResponse({'message':'NEED_ATHORIZATION'}, status=401)

        except KeyError:
            return JsonResponse({'message':'WRONG_KEY'}, status=400)

class SignInView(View):
    def post(self, request):
        input_data=json.loads(request.body)
        try:	
            if User.objects.filter(email=input_data['email']).exists():
                user_in_db=User.objects.get(email=input_data['email'])
                #패스워드 일치 확인
                if bcrypt.checkpw(input_data['password'].encode('utf-8'), user_in_db.password.encode('utf-8')):
                    #토큰 발행
                    user_token=jwt.encode({'id':user_in_db.id}, SECRET_KEY, algorithm='HS256').decode('utf-8')
			
                    return JsonResponse(
                                    {
                                        'message':'SUCCESS',
                                        'user_token':  f'{user_token}'
                                    },status=200
                                        )
                #패스워드가 일치하지 않음
                else:
				
                    return JsonResponse({'message':'INVALID_PASSWORD'}, status=409)
            else:
            #없는 유저이므로 401 Unauthorized
                return JsonResponse({'message':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message':'WRONG_KEY'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

class AuthSmsSendView(View):
    def send_sms(self, phone_number, auth_number):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-auth-key': f'{SMS_ACCESS_KEY_ID}',
            'x-ncp-service-secret':f'{SMS_SERVICE_SECRET}',
        }

        data = {
            'type':'SMS',
            'contentType':'COMM',
            'countryCode':'82',
            'from':f'{SMS_MY_PHONE_NUMBER}',
            'to':[
                f'{phone_number}',
            ],
            'content':f'요기용 인증번호 [{auth_number}]'
        }
        
        requests.post(SMS_URL, headers=headers, json=data)

    def post(self, request):
        try:
            input_data          = json.loads(request.body)
            created_auth_number = randint(1000, 10000)
            AuthSms.objects.update_or_create(phone_number=input_data['phone_number'],defaults={'phone_number':input_data['phone_number'],'auth_number':created_auth_number})
            self.send_sms(phone_number = input_data['phone_number'], auth_number = created_auth_number)

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'WRONG_KEY'}, status=400)

class AuthNumberConfirmView(View):
    def post(self, request):
        try:
            input_data         = json.loads(request.body)
            auth_record_in_db  = AuthSms.objects.get(phone_number=input_data['phone_number'])
            auth_number_in_db  = auth_record_in_db.auth_number
           
            if auth_number_in_db == int(input_data['auth_number']):
                return JsonResponse({'message':'SUCCESS', 'authorized_phone_number':input_data['phone_number']}, status=200)
            return JsonResponse({'message':'NOT_EXACT_VALUE', 'auth':False}, status=400)

        except KeyError:
            return JsonResponse({'message':'WRONG_KEY', 'auth':False}, status=400)

        except AuthSms.DoesNotExist:
            return JsonResponse({'message':'NEED_AUTHENTICATION_REQUEST', 'auth':False}, status=401)

class UserOrderHistoryView(View):
    @LoginConfirm
    def get(self, request):
        order_history_of_user = list(Order.objects.filter(user_id=request.user.id).order_by('-id').values())
        KST = timezone(timedelta(hours=9))
        for order in order_history_of_user:
            order_time_kst             = order['created_at'].replace(tzinfo=KST)
            order_time_kst             = order_time_kst + timedelta(hours=9)
            order['created_at']        = order_time_kst

            order['restuarant_name']   = Restaurants.objects.get(id=order['restaurant_id']).name
            
            menu_amount_infos_of_order = list(JoinOrderMenu.objects.filter(order_id=order['id']).values())
            order['menus'] = list()
            for menu in menu_amount_infos_of_order:
                menu_info           = dict()
                menu_instance       = Menus.objects.get(id=menu['menu_id'])
                menu_info['name']   = menu_instance.name
                menu_info['price']  = menu_instance.price
                menu_info['id']     = menu['menu_id']
                menu_info['amount'] = menu['amount']
                order['menus'].append(menu_info)
        return JsonResponse(order_history_of_user, status=200, safe=False)
