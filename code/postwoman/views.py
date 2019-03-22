from django.db import IntegrityError, transaction
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from postwoman.serializers import (LetterSerializer, PostWomanSerializer,
                                   PostOfficeSerializer,
                                   PlaceToVisitSerializer,
                                   RouteSerializer)
from postwoman.models import (PostWoman, PostOffice, Letter,
                              PlaceToVisit, Route)
from postwoman.route import calculate_route


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


class PlaceToVisitViewSet(BaseViewSet):
    queryset = PlaceToVisit.objects.all().order_by('name')
    serializer_class = PlaceToVisitSerializer


class RouteViewSet(BaseViewSet):
    queryset = Route.objects.all().order_by('-date')
    serializer_class = RouteSerializer
    http_method_names = ['post', 'get']

    def create(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            date = serializer.validated_data['date']
            postwoman = serializer.validated_data['postwoman']
            letters = list(Letter.objects.filter(postwoman=postwoman.id,
                                                 delivered=False,
                                                 date=date))
            places_to_visit = list(PlaceToVisit.objects.filter(
                postwoman=postwoman.id,
                visited=False))

            try:
                route = calculate_route(postwoman.postoffice, letters,
                                        places_to_visit,
                                        postwoman.max_distance)
            except Exception:
                return Response({'error': 'Error during calculate the route'},
                                status=status.HTTP_400_BAD_REQUEST)

            places_visited = []
            for node in route['route']:
                if node['type'] == 'PlaceToVisit':
                    places_visited.append(node['id'])
            try:
                with transaction.atomic():
                    if places_visited:
                        PlaceToVisit.objects.filter(
                            id__in=places_visited).update(visited=True)
                    Letter.objects.filter(postwoman=postwoman.id,
                                          delivered=False,
                                          date=date).update(delivered=True)
                    serializer.save(route=route)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'IntegrityError'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
