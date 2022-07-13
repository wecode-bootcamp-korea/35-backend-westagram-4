from django.db import models

class Posting(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='postings')
    image      = models.CharField(max_length=300)
    content    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'postings'