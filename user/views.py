import json
from django.http import JsonResponse
from django.views import View
import bcrypt
import jwt
from .models import Users

class SignUpView(View):
	def post(self, request):
		input_data=json.loads(request.body)
		#checking already signed up customer
		if not Users.objects.filter(email=input_data['email']).exists():
			#encrypting password
			encoded_password=input_data['password'].encode('utf-8')
			hashed_password=bcrypt.hashpw(encoded_password, bcrypt.gensalt())
			#storing in DB
			Users(
				email=input_data['email'],
				password=hashed_password.decode('utf-8'), #CharField이기 때문에 unicode로 넣어줌
				nickname=input_data['nickname'],
			).save()
			return JsonResponse({'message':'Sign UP SUCCESS'}, status=200)
		#Already Signed up customer
		else:
			#이미 존재하는 유저이므로 409 conflict
			return JsonResponse({'message':'Already Signed Up Account'}, status=409)

class SignInView(View):
	def get(self, request):
		input_data=json.loads(request.body)
		#Check email
		if Users.objects.filter(email=input_data['email']).exists():
			user_in_db=Users.objects.get(email=input_data['email'])
			#패스워드 일치 확인
			if bcrypt.checkpw(input_data['password'].encode('utf-8'), user_in_db.password.encode('utf-8')):
				token=jwt.encode({'id':user_in_db.id}, 'secret', algorithm='HS256')
				return JsonResponse({'message':f'Hi, {user_in_db.nickname}',
									 'token':  f'{token}'},
									  status=200)
			#패스워드가 일치하지 않음
			else:
				return JsonResponse({'message':'PASSWORD DOES NOT MATCH'}, status=409)
		else:
			#없는 유저이므로 401 Unauthorized
			return JsonResponse({'message':'INVALID_USER'}, status=401)
