from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=50)
    email        = models.CharField(max_length=50)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)

    class Meta:
        db_table = 'users'