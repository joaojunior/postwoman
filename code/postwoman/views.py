from rest_framework import viewsets, permissions

from postwoman.serializers import (PostWomanSerializer, PostOfficeSerializer,
                                   LetterSerializer)
from postwoman.models import PostWoman, PostOffice, Letter


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class PostWomanViewSet(BaseViewSet):
    queryset = PostWoman.objects.all().order_by('name')
    serializer_class = PostWomanSerializer


class LetterViewSet(BaseViewSet):
    queryset = Letter.objects.all().order_by('-date', 'latitude', 'longitude')
    serializer_class = LetterSerializer


class PostOfficeViewSet(BaseViewSet):
    queryset = PostOffice.objects.all().order_by('name')
    serializer_class = PostOfficeSerializer
