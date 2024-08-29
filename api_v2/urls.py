from django.urls import path

from api_v2.views import get_csrf_token

app_name = 'api_v2'

urlpatterns = [
    path('get-token/', get_csrf_token, name='get_token'),
]