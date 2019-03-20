from rest_framework import serializers

from postwoman.models import PostWoman, PostOffice, Letter


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
