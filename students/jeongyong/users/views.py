import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from my_settings  import SECRET_KEY , ALGORITHM
from .models      import User


class SignUpView(View):
    def post(self, request):
        try :    
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            contact  = data['contact']
            password = data['password']
       
            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' , email) :
                return JsonResponse({'messasge':'Invalid Email'}, status=400)
        
            if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$" , password) :
                return JsonResponse({'messasge':'Invalid Password'}, status=400)

            if User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'Email is exist'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                name     = name,
                password = hashed_password.decode('utf-8'),
                email    = email,
                contact  = contact,
            )    
      
            return JsonResponse({'messasge':'Success'}, status=201)
        
        except KeyError :
            return JsonResponse({'messasge':'KEY ERROR'}, status=400)    

class SignInView(View) :
    def post(self, request): 
        data = json.loads(request.body)
        try: 
            email    = data['email']
            password = data['password']
            user = User.objects.get(email=email)


            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'messasge':'INVALID_USER'}, status=401)

            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM)    
            return JsonResponse({'messasge':'SUCCESS',"access_token" : access_token}, status= 200)

        except KeyError: 
            return JsonResponse({'messasge':'KEY ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'messasge':'INVALID_USER'}, status=401)
