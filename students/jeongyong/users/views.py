import json
import re

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

            User.objects.create(
                name     = name,
                password = password,
                email    = email,
                contact  = contact,
            )    
      
            return JsonResponse({'messasge':'Success'}, status=201)
        
        except KeyError :
            return JsonResponse({'messasge':'KEY ERROR'}, status=400)    
