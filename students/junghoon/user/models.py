from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=50)
    email      = models.CharField(max_length=50, unique=True)
    password   = models.CharField(max_length=200)
    contact    = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.name
