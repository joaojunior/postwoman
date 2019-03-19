from django.db import models
from django.utils.timezone import now


class PostWoman(models.Model):
    name = models.CharField(max_length=200, unique=True)
    max_distance = models.FloatField(default=10)


class Letter(models.Model):
    latitude = models.FloatField(default=0)
    longitute = models.FloatField(default=0)
    date = models.DateField(default=now)
    delivered = models.BooleanField(default=False)
    postman = models.ForeignKey(PostWoman, on_delete=models.CASCADE)
