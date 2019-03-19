from rest_framework import serializers

from postwoman.models import PostWoman


class PostWomanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostWoman
        fields = ('name', 'max_distance')
