from api.views import CarViewSet, CommentViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'
api_v1 = DefaultRouter()
api_v1.register(r'cars', CarViewSet, basename='cars')
api_v1.register(
    r'cars/(?P<car_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('', include(api_v1.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
