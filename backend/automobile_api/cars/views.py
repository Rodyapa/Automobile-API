from django.views.generic import ListView
from cars.models import Car


class HomepageListView(ListView):
    template_name = "cars/index.html"

    def get_queryset(self):
        queryset = (
            Car.objects.all()
            .select_related('owner')
        )
        return queryset

    ordering = "created_at"
