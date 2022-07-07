from django.db import models

class User(models.Model):
    user_name     = models.CharField(max_length=50)
    user_email    = models.CharField(max_length=200 , unique=True)
    user_password = models.CharField(max_length=200)
    user_contact  = models.CharField(max_length=150)

    class Meta:
        db_table = 'users'
