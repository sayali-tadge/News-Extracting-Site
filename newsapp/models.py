from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model

# Create your models here.
# Model for storing keyword history and response generated
class History(models.Model):
    user =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    keyword = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null= True)

# Create a a model to assign per usage quota for user.
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50, null = True)
    User_quota = models.PositiveIntegerField(default=15)

    def __str__(self):
        return self.user.username
    

def is_admin(user):
    return user.is_staff
