import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import User

class UserView(View):
    def post(self, request):
        """
        목적 : 회원가입 기능을 구현하고 들어오는 정보들을 DB에 저장한다.
        
        1. client로부터 받아야 하는 정보
            - 이름 / 이메일 / 비밀번호 / 연락처 / 그 외 개인정보?????
            
        2. 구현해야하는 로직
            - 이메일 or 패스워드 전달안된 경우
            - 이메일에 @와 . 들어갔는지
            - 비밀번호 조건 성립 여부
            - 이메일 중복 여부
        """
        
        data = json.loads(request.body)
        
        valid_email    = re.compile('^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$')
        valid_password = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
        
        if data['email'] == '' or data['password'] == '':
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        if not valid_email.match(data['email']):
            return JsonResponse({'message':'Email is invalid.'}, status=400)
         
        if not valid_password.match(data['password']):
            return JsonResponse({'message':'Password is invalid.'}, status=400)
        
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'message':'Email already in use.'}, status=400)
         
        User.objects.create(
            name          = data['name'],
            email         = data['email'],
            password      = data['password'],
            phone_number  = data['phone_number'],
        )
        
        return JsonResponse({'message':'SUCCESS'}, status=201)
        

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email_exist_user = User.objects.get(email=data['email'])
            
            if not email_exist_user:
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            
            if data['password'] != email_exist_user.password:
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            
            return JsonResponse({'message':'SUCCESS'}, status=200)
                  
        except:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)