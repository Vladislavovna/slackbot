from django.db import models

# Create your models here.

class Poll(models.Model):
    name = models.CharField(max_length=20)


class Question(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    text = models.TextField()

class SlackUser(models.Model):
    name =  models.CharField(max_length=20)
    email = models.CharField(max_length=60)
