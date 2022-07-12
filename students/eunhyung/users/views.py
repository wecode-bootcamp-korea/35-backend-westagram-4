import json
import re

import bcrypt
import jwt 
from django.conf import settings
from django.http  import JsonResponse
from django.views import View

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