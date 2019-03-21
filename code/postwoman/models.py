import uuid
from datetime import date

from django.db import models
from django.contrib.postgres import fields


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class PostOffice(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PostWoman(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    max_distance = models.FloatField(default=10)
    postoffice = models.ForeignKey(PostOffice, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Letter(BaseModel):
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    date = models.DateField(default=date.today)
    delivered = models.BooleanField(default=False)
    postwoman = models.ForeignKey(PostWoman, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('latitude', 'longitude', 'date', 'postwoman'),)
        indexes = [
            models.Index(fields=['date', 'postwoman'])
        ]


class PlaceToVisit(BaseModel):
    name = models.CharField(max_length=200)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    postwoman = models.ForeignKey(PostWoman, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'postwoman'),)


class Route(BaseModel):
    postwoman = models.ForeignKey(PostWoman, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    route = fields.JSONField()

    class Meta:
        unique_together = (('date', 'postwoman'),)
