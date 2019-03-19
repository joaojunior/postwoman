from django.db import models
from datetime import date


class PostWoman(models.Model):
    name = models.CharField(max_length=200, unique=True)
    max_distance = models.FloatField(default=10)


class Letter(models.Model):
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    date = models.DateField(default=date.today)
    delivered = models.BooleanField(default=False)
    postwoman = models.ForeignKey(PostWoman, on_delete=models.CASCADE)
