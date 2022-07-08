import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        
        data = json.loads(request.body)
        
        try:
            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            
            REGEX_EMAIL    = '^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(REGEX_EMAIL, data['email']):
                return JsonResponse({'message':'Email is invalid.'}, status=400)
            
            if not re.match(REGEX_PASSWORD, data['password']):
                return JsonResponse({'message':'Password is invalid.'}, status=400)
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'Email already in use.'}, status=400)
         
            User.objects.create(
                name          = name,
                email         = email,
                password      = password,
                phone_number  = phone_number
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
            
        except:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
    
        
    
        
       
        
        
        
