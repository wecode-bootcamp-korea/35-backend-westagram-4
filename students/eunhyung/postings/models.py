from django.db import models

class Posting(models.Model):
    name       = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=)   # 이미지???
    # 모델링 마저 작업해야함