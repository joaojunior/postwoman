from django.urls import include, path
from rest_framework import routers

from postwoman import views

router = routers.DefaultRouter()
router.register('postwoman', views.PostWomanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework'))
]
