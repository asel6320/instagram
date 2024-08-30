from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from api_v3.views import PostViewSet
from rest_framework import routers

app_name = 'api_v3'

router = routers.DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
]