import jwt
import json
import bcrypt
import requests
from random            import randint
from django.http       import JsonResponse
from django.views      import View
from .models           import User, AuthSms
from yogiyong.settings import SECRET_KEY, SMS_ACCESS_KEY_ID, SMS_URL, SMS_SERVICE_SECRET, SMS_MY_PHONE_NUMBER

class SignUpView(View):
    def post(self, request):
        input_data=json.loads(request.body)
        try:
            #존재하는 유저인지 체크
            if User.objects.filter(email=input_data['email']).exists():	
                #이미 존재하는 유저이므로 409 conflict		
                return JsonResponse({'message':'USER_EXISTS'}, status=409)
            else:
                #패스워드 암호화
                encoded_password = input_data['password'].encode('utf-8')
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                #DB에 저장
                User(
                    email = input_data['email'],
                    password = hashed_password.decode('utf-8'), #CharField이기 때문에 unicode로
                    nickname = input_data['nickname'],
                    notofocation_accept = input_data['notification_accept'],
                    #social_platform=,                    
                    ).save()
			
                return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'WRONG_KEY'}, status=400)

class SignInView(View):
    def post(self, request):
        input_data=json.loads(request.body)
        print(input_data)
        try:	
        #기존 회원인지 확인
            if User.objects.filter(email=input_data['email']).exists():
                user_in_db=User.objects.get(email=input_data['email'])
                #패스워드 일치 확인
                if bcrypt.checkpw(input_data['password'].encode('utf-8'), user_in_db.password.encode('utf-8')):
                    #토큰 발행
                    user_token=jwt.encode({'id':user_in_db.id}, SECRET_KEY, algorithm='HS256')
			
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
    #실제 문자를 보내주는 메서드
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
            input_phone_number  = input_data['phone_number']
            created_auth_number = randint(1000, 10000)
            exist_phone_number             = AuthSms.objects.get(phone_number=input_phone_number)
            exist_phone_number.auth_number = created_auth_number
            exist_phone_number.save()
            #sms 보내기
            self.send_sms(phone_number = input_phone_number, auth_number = created_auth_number)
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except AuthSms.DoesNotExist:
            AuthSms.objects.create(
                            phone_number = input_phone_number,
                            auth_number  = created_auth_number
                            ).save()
            #sms 보내기
            self.send_sms(phone_number = input_phone_number, auth_number = created_auth_number)
            return JsonResponse({'message':'SUCCESS'}, status=200)

class AuthNumberConfirmView(View):
    def post(self, request):
        try:
            input_data         = json.loads(request.body)
            input_phone_number = input_data['phone_number']
            input_auth_number  = input_data['auth_number']
            auth_record_in_db  = AuthSms.objects.get(phone_number=input_phone_number)
            auth_number_in_db  = auth_record_in_db.auth_number
           
            if auth_number_in_db == int(input_auth_number):
                return JsonResponse({'message':'SUCCESS', 'auth':'True'}, status=200)
            return JsonResponse({'message':'NOT_EXACT_VALUE', 'auth':'False'}, status=400)

        except KeyError:
            return JsonResponse({'message':'WRONG_KEY', 'auth':'False'}, status=400)
        except AuthSms.DoesNotExist:
            return JsonResponse({'message':'NO_AUTHENTICATION_REQUEST', 'auth':'False'}, status=401)
