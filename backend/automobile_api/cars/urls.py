from cars import views
from django.urls import include, path

app_name = 'cars'

cars_url_patterns = [
    path("<int:pk>/", views.car_detail, name="car-detail"),
    path("create/", views.CarCreateView.as_view(), name='car-create'),
    path("<int:pk>/edit/", views.CarUpdateView.as_view(), name='car-edit'),
    path("<int:pk>/delete/", views.CarDeleteView.as_view(), name='car-delete'),
    path("<int:pk>/comment/", views.add_comment, name="add_comment")
]
urlpatterns = [
    path('', views.HomepageListView.as_view(), name='index'),
    path("cars/", include(cars_url_patterns)),
]
