from django.urls import include, path
from rest_framework import routers

from postwoman import views

router = routers.DefaultRouter()
router.register('postwoman', views.PostWomanViewSet)
router.register('postoffice', views.PostOfficeViewSet)
router.register('letter', views.LetterViewSet)
router.register('placetovisit', views.PlaceToVisitViewSet)
router.register('route', views.RouteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework'))
]
