from django.db import models


class PostWoman(models.Model):
    name = models.CharField(max_length=200, unique=True)
    max_distance = models.FloatField(default=10)
