import json
import re
import bcrypt

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
            
            salt            = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
            
            REGEX_EMAIL    = '^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(REGEX_EMAIL, data['email']):
                return JsonResponse({'message':'Email is invalid.'}, status=400)
            
            if not re.match(REGEX_PASSWORD, data['password']):
                return JsonResponse({'message':'Password is invalid.'}, status=400)
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'Email already in use.'}, status=400)
         
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
        data = json.loads(request.body)

        try: 
            if not User.objects.filter(email=data['email']).exists() :
                return JsonResponse({"message": "INVALID_USER"}, status = 401)   

            if User.objects.filter(email=data['email']):
                if User.objects.filter(password=data['password']):
                    return JsonResponse({"message": "SUCCESS"}, status = 200) 
                else:
                    return JsonResponse({"message": "INVALID_USER"}, status = 401) 

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)