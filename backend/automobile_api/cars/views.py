from django.views.generic import ListView
from cars.models import Car, Comment
from django.shortcuts import get_object_or_404, render


class HomepageListView(ListView):
    template_name = "cars/index.html"

    def get_queryset(self):
        queryset = (
            Car.objects.all()
            .select_related('owner')
        )
        return queryset

    ordering = "created_at"


def post_detail(request, pk):
    template_name = "cars/detail.html"
    car = get_object_or_404(Car.objects.all(), pk__exact=pk)
    comments = (
        Comment.objects.all()
        .filter(car=car)
        .select_related("author")
        .order_by("created_at")
    )
    context = {"car": car}
    # #context["form"] = CommentsForm()
    context["comments"] = comments
    return render(request, template_name, context)
