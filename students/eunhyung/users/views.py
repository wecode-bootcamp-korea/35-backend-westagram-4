import bcrypt
import json
import re
import jwt  # 패키지 설치는 pyjwt지만 import 모듈 이름은 jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        
        data = json.loads(request.body)
        
        try:
            name            = data['name']
            email           = data['email']
            phone_number    = data['phone_number']
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            
            REGEX_EMAIL    = '^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message':'Email is invalid.'}, status=400)
            
            if not re.match(REGEX_PASSWORD, data['password']):
                return JsonResponse({'message':'Password is invalid.'}, status=400)
            
            if User.objects.filter(email=email).exists():
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
        try:
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']
            
            email_exist_user = User.objects.get(email=email)
                    
            # 해시화된 비밀번호와 들어온 비밀번호 해시한 결과값이 같은지 비교하기
            # if password != email_exist_user.password:
            # DB에 저장된 string도 인코딩 , 클라이언트가 입력한 password string도 인코딩해서 비교해야함
            # 그 값이 false라면 틀리단 이야기
            if not bcrypt.checkpw(password.encode('utf-8'), email_exist_user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            
            # 코드가 이쪽으로 넘어오면, 비밀번호가 일치한단 이야기
            # 그러면 JWT발급하고, 응답에 담아 보내기
            SECRET = SECRET_KEY
            user_token = jwt.encode({'user_id':email_exist_user.id}, SECRET, algorithm='HS256')
            return JsonResponse({'token':user_token}, status=200)
                  
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)