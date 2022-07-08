from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=50)
    email      = models.CharField(max_length=200 , unique=True)
    password   = models.CharField(max_length=200)
    contact    = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    updated_at = models.DateTimeField(auto_now=True , null=True)

    class Meta:
        db_table = 'users'
