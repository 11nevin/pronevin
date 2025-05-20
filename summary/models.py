from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Login(AbstractUser):
    user_type = models.CharField(max_length = 50,null=True)
    joined_date = models.DateTimeField(auto_now_add=True,null=True)
    premium = models.BooleanField(default=False)
    premium_date = models.DateField(null = True)
    question = models.CharField(max_length= 100,null=True)
    answer = models.CharField(max_length= 100,null=True)
  
    

class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length = 50)
    email = models.EmailField()
    contact= models.IntegerField()
    age = models.IntegerField()
    qualification = models.CharField(max_length=10)
    purpose = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    loginid = models.ForeignKey(Login,on_delete=models.CASCADE,null=True)

class Video_History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.CharField(max_length=200,null=True)
    summary = models.CharField(max_length=700)
    date_time = models.DateTimeField(auto_now_add=True)

class Text_History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text_input = models.CharField(max_length=700)
    summary = models.CharField(max_length=700)
    date_time = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.CharField(max_length=200)
    reply = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True,null=True)

class Premium(models.Model):
    months = models.IntegerField()
    real_price = models.FloatField()
    offer_price=models.FloatField(null=True)
    offer_started = models.DateTimeField(auto_now_add=True)
    offer_till=models.DateTimeField(null=True)


class News(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    genre = models.CharField(max_length=50,null=True)
    timing = models.FloatField(null=True)
    likes = models.IntegerField(default=0)
    title = models.CharField(max_length=5000,null=True)


