import json
import re
import bcrypt

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body) 

        REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

        try :
            name            = data['name']
            email           = data['email']
            username        = data['username']
            password        = data['password']
            phone_number    = data['phone_number']
            hash_password   = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            decode_password = hash_password.decode('utf-8')

            if not re.match(REGEX_EMAIL, data['email']) :
                return JsonResponse({"message": "Invalid email format"}, status = 400)   

            if not re.match(REGEX_PASSWORD, data['password']):
                return JsonResponse({"message": "Invalid password format"}, status = 400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "Already registered Email"}, status = 400)   
            
            User.objects.create(
                name         = name,
                email        = email,
                username     = username,
                password     = decode_password,
                phone_number = phone_number,
            )
            return JsonResponse({"message": "SUCCESS"}, status = 201)
            
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try: 
            if not User.objects.filter(email=data['email']).exists() :
                return JsonResponse({"message": "INVALID_USER"}, status = 401)   

            if not User.objects.filter(email=data['email'], password=data['password']):
                return JsonResponse({"message": "INVALID_USER"}, status = 401)
                
            return JsonResponse({"message": "SUCCESS"}, status = 200) 

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)