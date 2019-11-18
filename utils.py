import jwt
import json
from user.models       import User
from yogiyong.settings import SECRET_KEY
from django.http       import JsonResponse

class TestFunction:
    def __init__(self, info1, info2):
        self.info1 = info1
        self.info2 = info2
    
    def __call__(self, a, b):
        return {a : self.info1, b : self.info2}

test_function = TestFunction("1", "2")
test_function(1, 2)
==> {1 : "1", 2 : "2"}

test_function2 = TestFunction("3", "4")
test_function(1, 2)
==> {1 : "3", 2 : "4"}

## named tuple
(1,2)
c = (1, 2)
c[0]
c[1]

Cord = NamedTuple("cord", "x y")
c = Cord(1, 2)

c.x 
c.y 



def test_function(a, b, info1, info2)
    return {a : self.info1, b : self.info2}

class LoginConfirm:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        token      = request.headers.get("Authorization", None)
        secret_key = SECRET_KEY
        try:
            if token:
                token_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
                user_id       = token_payload['id']
                user          = User.objects.get(id=user_id)
                request.user  = user
                return self.original_function(self, request, *args, **kwargs)

            return JsonResponse({'messaege':'NEED_LOGIN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

class OrderLoginConfirm:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        token      = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token.encode('utf-8'), SECRET_KEY, algorithms=['HS256'])
                user_id       = token_payload['id']
                user          = User.objects.get(id=user_id)
                request.user  = user
                return self.original_function(self, request, *args, **kwargs)

            request.user = None
            return self.original_function(self, request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
