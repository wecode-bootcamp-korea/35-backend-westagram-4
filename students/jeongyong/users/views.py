import json
import re
import bcrypt

from django.http import JsonResponse
from django.views import View

from .models import User


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
                password = hashed_password.decode(),
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

            if not User.objects.filter(email=email, password=password).exists(): 
                return JsonResponse({'messasge':'INVAILD_USERS'}, status=401)
            return JsonResponse({'messasge':'SUCCESS'}, status=200)
            
        except KeyError: 
            return JsonResponse({'messasge':'KEY ERROR'}, status=400)