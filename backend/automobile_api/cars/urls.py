from django.urls import path
from cars.views import HomepageListView

urlpatterns = [
    path('', HomepageListView.as_view(), name='index'),
]
