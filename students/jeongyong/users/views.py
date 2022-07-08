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
                return JsonResponse({'messasge':'이메일 형식에 맞지 않습니다.'}, status=400)
        
            if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$" , password) :
                return JsonResponse({'messasge':'비밀번호 형식에 맞지 않습니다.'}, status=400)

            if User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'존재하는 이메일 입니다.'}, status=400)

            User.objects.create(
                name     = name,
                password = password,
                email    = email,
                contact  = contact,
            )    
      
            return JsonResponse({'messasge':'회원가입 완료'}, status=201)
        
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