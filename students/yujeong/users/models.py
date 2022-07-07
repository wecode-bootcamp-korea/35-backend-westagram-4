from django.db import models

class User(models.Model) :
    user_name         = models.CharField(max_length = 20)
    user_email        = models.EmailField(max_length = 45)
    user_id           = models.CharField(max_length = 50)
    user_pw           = models.CharField(max_length=20)
    user_phone_number = models.CharField(max_length = 50)
    
    class Meta :
        db_table = 'users'