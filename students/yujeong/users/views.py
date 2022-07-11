import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body) 

        REGEX_EMAIL    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        REGEX_PASSWORD = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

        try :
            if not REGEX_EMAIL.match(data['email']) :
                return JsonResponse({"message": "Invalid email format"}, status = 400)   

            if not REGEX_PASSWORD.match(data['password']):
                return JsonResponse({"message": "Invalid password format"}, status = 400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "Already registered Email"}, status = 400)   
            
            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                username     = data['username'],
                password     = data['password'],
                phone_number = data['phone_number'],
            )
            return JsonResponse({"message": "SUCCESS"}, status = 201)
            
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)       