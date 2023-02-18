from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    score = models.IntegerField()
    attempted = models.DateTimeField(auto_now_add=True)
    ques = models.JSONField()
    params = models.JSONField()

class settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    add = models.BooleanField(default=True)
    sub = models.BooleanField(default=True)
    mul = models.BooleanField(default=True)
    div = models.BooleanField(default=True)
    duration = models.PositiveIntegerField(default=120)
    add_left_min = models.PositiveIntegerField(default=2)
    add_left_max = models.PositiveIntegerField(default=100)
    add_right_min = models.PositiveIntegerField(default=2)
    add_right_max = models.PositiveIntegerField(default=100)
    mul_left_min = models.PositiveIntegerField(default=2)
    mul_left_max = models.PositiveIntegerField(default=12)
    mul_right_min = models.PositiveIntegerField(default=2)
    mul_right_max = models.PositiveIntegerField(default=100)