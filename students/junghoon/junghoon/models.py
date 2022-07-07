from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.CharField(max_length=200, help_text='최대 200글자 내로 입력하세요.', unique=True)
    password   = models.TextField(null=True)
    contact    = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.name
