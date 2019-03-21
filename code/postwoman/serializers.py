from rest_framework import serializers

from postwoman.models import (Letter, PostWoman, PostOffice,
                              PlaceToVisit, Route)


class PostWomanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostWoman
        fields = ('name', 'max_distance', 'postoffice')


class LetterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Letter
        fields = ('latitude', 'longitude', 'date', 'delivered', 'postwoman')


class PostOfficeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostOffice
        fields = ('name', 'latitude', 'longitude')


class PlaceToVisitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlaceToVisit
        fields = ('name', 'latitude', 'longitude', 'postwoman')


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Route
        fields = ('date', 'postwoman', 'route')
        read_only_fields = ('route',)
