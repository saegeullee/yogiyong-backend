import jwt
import json
import bcrypt
import requests

from datetime          import datetime, timedelta, timezone
from random            import randint
from django.http       import JsonResponse
from django.views      import View
from .models           import User, AuthCode
from yogiyong.settings import SECRET_KEY, SMS_ACCESS_KEY_ID, SMS_URL, SMS_SERVICE_SECRET, SMS_MY_PHONE_NUMBER
from utils             import LoginConfirm
from order.models      import Order, JoinOrderMenu
from restaurant.models import Restaurants, Menus

class SignUpView(View):
    def post(self, request):
        input_data = json.loads(request.body)

        try:
            phone_number = input_data['authorized_phone_number']

            if not AuthorizedPhoneNumber.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'error':'UNCONFIRMED_NUMBER'}, status=400)
            
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
                    
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({'message':'INVALID_INPUT'}, status=400)

class SignInView(View):
    def post(self, request):
        input_data = json.loads(request.body)

        try:	
            user = User.objects.get(email=input_data['email'])

            if bcrypt.checkpw(
                input_data['password'].encode('utf-8'),
                user.password.encode('utf-8')
            ):
                user_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256').decode('utf-8')
                return JsonResponse({'access_token' : user_token}, status=200)
            
            return JsonResponse({'message':'INVALID_PASSWORD'}, status=409)
        except KeyError:
            return JsonResponse({'message':'WRONG_KEY'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

class AuthCode(View):
    def send_sms(self, phone_number, auth_number):
        headers = {
            'Content-Type'         : 'application/json; charset=utf-8',
            'x-ncp-auth-key'       : f'{SMS_ACCESS_KEY_ID}',
            'x-ncp-service-secret' : f'{SMS_SERVICE_SECRET}',
        }

        data = {
            'type'        : 'SMS',
            'contentType' : 'COMM',
            'countryCode' : '82',
            'from'        : SMS_MY_PHONE_NUMBER,
            'to'          : [phone_number],
            'content'     : f'요기용 인증번호 [{auth_number}]'
        }
        
        requests.post(SMS_URL, headers=headers, json=data, timeout=1)

    def post(self, request):
        try:
            input_data          = json.loads(request.body)
            created_auth_number = randint(1000, 10000)

            AuthCode.objects.create(
                phone_number = input_data['phone_number'],
                auth_number  = created_auth_number
            )

            resp = self.send_sms(
                phone_number = input_data['phone_number'],
                auth_number  = created_auth_number
            )

            if resp.status == 200:
                return HttpResponse(status=200)
            else:
                return JsonResponse({"error" : resp.text}, status=resp.status)
        except KeyError:
            return JsonResponse({'message':'WRONG_KEY'}, status=400)

class AuthCodeConfirmView(View):
    def post(self, request):
        try:
            input_data = json.loads(request.body)
            auth_code  = AuthCode.objects.get(phone_number = input_data['phone_number'])
           
            if auth_code.auth_number == int(input_data['auth_number']):
                return JsonResponse({'authorized_phone_number':input_data['phone_number']}, status=200)

            return JsonResponse({'message':'INVALID_AUTH_CODE'}, status=401)
        except KeyError:
            return JsonResponse({'message':'WRONG_KEY', 'auth':False}, status=400)
        except AuthCode.DoesNotExist:
            return JsonResponse({'message':'INVALID_AUTH_CODE'}, status=401)

class UserOrderHistoryView(View):
    @login_confirm
    def get(self, request):
        order_history = Order.objects.filter(user_id=request.user.id).select_related('restuarant').order_by('-id')

        order_history = [{
            "name" : order.name,
            "restuarant_name" : order.restaurant.name,
            ....,
            "menus" : order.menus.values()
        } for order in order_history]

        return JsonResponse(order_history_of_user, status=200, safe=False)
