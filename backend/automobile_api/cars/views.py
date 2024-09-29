from django.views.generic import ListView
from cars.models import Car, Comment
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from cars.forms import CommentForm


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
        .order_by("-created_at")
    )
    context = {"car": car}
    context["form"] = CommentForm()
    context["comments"] = comments
    return render(request, template_name, context)


@login_required
def add_comment(request, pk):
    car = get_object_or_404(Car, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.car = car
        comment.save()
    return redirect("cars:cars-detail", pk=pk)
