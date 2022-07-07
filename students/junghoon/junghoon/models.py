from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=45)
    email    = models.CharField(max_length=200)
    password = models.TextField()
    contact  = models.CharFiled(max_length=45)

    class Meta:
	db_table = 'Users'
	
    def __str__(self):
	return self.name
