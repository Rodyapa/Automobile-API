from django.urls import path, include
from cars import views

app_name = 'cars'

cars_url_patterns = [
    path("<int:pk>/", views.post_detail, name="cars-detail"),
    path("<int:pk>/comment/", views.add_comment, name="add_comment")
]
urlpatterns = [
    path('', views.HomepageListView.as_view(), name='index'),
    path("cars/", include(cars_url_patterns)),
]
