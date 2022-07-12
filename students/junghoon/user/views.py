import json
import re
import bcrypt

from django.http import JsonResponse
from django.views import View

from.models import User

class SignupView(View):
    def post(self, request):
        try:
            data                  = json.loads(request.body)
            name                  = data['name']
            password              = data['password']
            email                 = data['email']
            contact               = data['contact']
            REGEX_EMAIL           = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD        = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message': "EMAIL_IS_NOT_VALID"}, status=400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message": "PASSWORD_IS_NOT_VALID"}, status=401)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE": "EMAIL_ALREADY_EXISTS"}, status=401)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                name     = name,
                email    = email,
                password = hashed_password.decode('utf-8'),
                contact  = contact,
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']

            if User.objects.filter(email=email).exists():
                user_password = User.objects.get(email=email).password
                encoded_password = data['password'].encode('utf-8')

                if bcrypt.checkpw(encoded_password, user_password.encode('utf-8')):
                    return JsonResponse({'message': 'SUCCESS'}, status=200)

                else:
                    return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

            else:
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            # if User.objects.filter(email=data['email']).exists():
            #     user_password = User.objects.get(email=data['email']).password
            #     encoded_password = data['password'].encode('utf-8')
            #     if bcrypt.checkpw(encoded_password, user_password.encode('utf-8')):
            #         return JsonResponse({'message': 'SUCCESS'}, status=200)
            #     return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
            # return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
