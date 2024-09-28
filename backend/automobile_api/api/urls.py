from api.views import CarViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'
api_v1 = DefaultRouter()
api_v1.register(r'cars', CarViewSet, basename='cars')
urlpatterns = [
    path('', include(api_v1.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
