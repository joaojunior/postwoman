import uuid
from datetime import date

from django.db import models


class PostWoman(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    max_distance = models.FloatField(default=10)


class Letter(models.Model):
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    date = models.DateField(default=date.today)
    delivered = models.BooleanField(default=False)
    postwoman = models.ForeignKey(PostWoman, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('latitude', 'longitude', 'date'),)
        indexes = [
            models.Index(fields=['date', 'postwoman'])
        ]
