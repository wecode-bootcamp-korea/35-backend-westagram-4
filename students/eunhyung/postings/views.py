import json

from django.http import JsonResponse
from django.views import View

from users.models import User
from postings.models import Posting

class PostingView(View):
    def post(self, request):
        
        data = json.loads(request.body)
        
        try:
            user    = data['user_id']
            image   = data['image']
            content = data['content']
            
            if not User.objects.filter(id=user).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=401)
        
            Posting.objects.create(
                user    = User.objects.get(id=user),
                image   = image,
                content = content
            )
        
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
            