from rest_framework import viewsets, permissions

from postwoman.serializers import PostWomanSerializer, LetterSerializer
from postwoman.models import PostWoman, Letter


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class PostWomanViewSet(BaseViewSet):
    queryset = PostWoman.objects.all().order_by('name')
    serializer_class = PostWomanSerializer


class LetterViewSet(BaseViewSet):
    queryset = Letter.objects.all().order_by('-date', 'latitude', 'longitude')
    serializer_class = LetterSerializer
