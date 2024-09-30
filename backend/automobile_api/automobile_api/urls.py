from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from users.forms import CustomUserCreationForm

schema_view = get_schema_view(
    openapi.Info(
        title="Automobile-API-DOCS",
        default_version='v1',
        description="",
        terms_of_service="",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

docs_urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('openapi/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
]

auth_urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("registration/", CreateView.as_view(
        template_name="registration/registration_form.html",
        form_class=CustomUserCreationForm,
        success_url=reverse_lazy("cars:index"),
    ), name="registration"),
]

urlpatterns = [
    path('', include('cars.urls'), name='cars'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'), name='api'),
    path('docs/', include(docs_urlpatterns), name='docs'),
    path('auth/', include(auth_urlpatterns), name='auth')
]
