import json
import re

import bcrypt
import jwt 
from django.http  import JsonResponse
from django.views import View

# from my_settings  import ALGORITHM, SECRET_KEY   
# ALGORITHM, SECRET_KEY와 같은 환경변수를 my_settings.py파일로 관리하고 있다.
# my_settings.py파일은 환경변수 관리로서의 역할만 하는 파일이다. 
# 따라서 import해서 사용하면 my_settings.py파일에 의존하게 되므로, 의존성이 생긴다.

# 만약 환경변수를 my_settings.py파일이 아니라 다른 방법으로 관리한다면?
# 만약 파일 이름이 my_settings가 아니라 your_settings가 된다면?
# import한 부분의 코드들을 모두 바까줘야한다.

# 그러니까 my_settings에서 불러오지말고, 수정되어도 아무 지장이 없도록
from django.conf import settings
# 를 사용해서 가져오자.

from users.models import User

class SignUpView(View):
    def post(self, request):
        
        data = json.loads(request.body)
        
        try:
            name         = data['name']
            email        = data['email']
            phone_number = data['phone_number']
            password     = data['password']
            
            REGEX_EMAIL    = '^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message':'Email is invalid.'}, status=400)
            
            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'message':'Password is invalid.'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'Email already in use.'}, status=400)
         
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
         
            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_password.decode('utf-8'),
                phone_number = phone_number
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
    

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']
            
            email_exist_user = User.objects.get(email=email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), email_exist_user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            
            user_token = jwt.encode({'user_id':email_exist_user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            
            return JsonResponse({'token':user_token}, status=200)
                  
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)  