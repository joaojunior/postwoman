from rest_framework import serializers

from postwoman.models import PostWoman
from postwoman.models import Letter


class PostWomanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostWoman
        fields = ('name', 'max_distance')


class LetterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Letter
        fields = ('latitude', 'longitude', 'date', 'delivered', 'postwoman')
