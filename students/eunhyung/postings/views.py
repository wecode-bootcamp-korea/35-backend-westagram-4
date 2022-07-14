import json

from django.http import JsonResponse
from django.views import View

from users.models import User
from postings.models import Posting

class PostingView(View):
    def post(self, request):
        """
        게시글 발행 기능
        
        # user_id가 존재하는지 확인
        """
        data = json.loads(request.body)
        
        try:
            
            if not User.objects.filter(id=data['user_id']).exists():
                return JsonResponse({'message':'유저 아이디 없음'}, status=400)
            
        
            Posting.objects.create(
                user    = User.objects.get(id=data['user_id']),
                image   = data['iamge'],
                content = data['content']
            )
        
            return JsonResponse({'message':'성공!'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
            