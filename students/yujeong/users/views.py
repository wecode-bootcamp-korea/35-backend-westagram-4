import json
import re

import bcrypt
import jwt
from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body) 

        try :
            name         = data['name']
            email        = data['email']
            username     = data['username']
            password     = data['password']
            phone_number = data['phone_number']

            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message": "Invalid email format"}, status = 400)   

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message": "Invalid password format"}, status = 400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Already registered Email"}, status = 400)   

            hash_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
            
            User.objects.create(
                name         = name,
                email        = email,
                username     = username,
                password     = hash_password,
                phone_number = phone_number,
            )
            return JsonResponse({"message": "SUCCESS"}, status = 201)
            
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try: 
            email    = data['email']
            password = data['password'] 

            user = User.objects.get(email=email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
               return JsonResponse({"message": "INVALID_USER_Password error"}, status = 401)    
   
            access_token = jwt.encode({"id": user.id }, SECRET_KEY, ALGORITHM)
                
            return JsonResponse({"message": access_token}, status = 200)

        except User.DoesNotExist:               
            return JsonResponse({"message": "INVALID_USER _not macth"}, status = 400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)