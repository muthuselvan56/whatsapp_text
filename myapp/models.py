from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=10,unique=True)
    message = models.TextField(default='-')
 
    def __str__(self):
        return self.name
