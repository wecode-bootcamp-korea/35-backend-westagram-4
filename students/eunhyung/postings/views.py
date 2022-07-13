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
            user    = data['user_id']
            image   = data['image']
            content = data['content']
            
            if not User.objects.get(user_id=user):
                return JsonResponse({'message':'User is not exist'}, status=401)
        
            Posting.objects.create(
                user    = user,
                image   = image,
                content = content
            )
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
            