from rest_framework import viewsets, permissions

from postwoman.serializers import PostWomanSerializer
from postwoman.models import PostWoman


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class PostWomanViewSet(BaseViewSet):
    queryset = PostWoman.objects.all().order_by('name')
    serializer_class = PostWomanSerializer
