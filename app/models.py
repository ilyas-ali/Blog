from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    #num=models.IntegerField()
    detail=models.TextField(null=True)
    image=models.FileField()
    permit=models.BooleanField(default=True)

    #def __str__(self):
     #   return self.detail
   
    