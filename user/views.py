import jwt
import json
import bcrypt
from django.http  import JsonResponse
from django.views import View
from .models	  import User

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
                Users(
                    email = input_data['email'],
                    password = hashed_password.decode('utf-8'), #CharField이기 때문에 unicode로
                    nickname = input_data['nickname'],
                    email_accept = input_data['email_accept'],
                    #social_platform=,                    
                    ).save()
			
                return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'WRONG_KEY'}, status=400)

class SignInView(View):
    def get(self, request):
        input_data=json.loads(request.body)
        try:	
        #기존 회원인지 확인
            if User.objects.filter(email=input_data['email']).exists():
                user_in_db=User.objects.get(email=input_data['email'])
                #패스워드 일치 확인
                if bcrypt.checkpw(input_data['password'].encode('utf-8'), user_in_db.password.encode('utf-8')):
                    #토큰 발행
                    token=jwt.encode({'id':user_in_db.id}, 'secret', algorithm='HS256')
			
                    return JsonResponse(
                                        {
                                            'message':'SUCCESS',
                                            'token':  f'{token}'
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
