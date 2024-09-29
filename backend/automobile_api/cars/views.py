from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from cars.models import Car, Comment
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from cars.forms import CommentForm, CarForm


class HomepageListView(ListView):
    template_name = "cars/index.html"

    def get_queryset(self):
        queryset = (
            Car.objects.all()
            .select_related('owner')
        )
        return queryset


def car_detail(request, pk):
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


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = "cars/create.html"

    def get_success_url(self):
        return reverse_lazy(
            "cars:index"
        )

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = "cars/create.html"
    success_url = reverse_lazy("cars:index")

    def dispatch(self, request, *args, **kwargs):
        car = get_object_or_404(Car, pk=kwargs["pk"])
        if not request.user.is_authenticated:
            return redirect("cars:car-detail", pk=kwargs["pk"])
        if request.user != car.owner:
            return redirect("cars:car-detail", pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    form_class = CarForm
    template_name = "cars/create.html"
    success_url = reverse_lazy("cars:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context

    def dispatch(self, request, *args, **kwargs):
        car = get_object_or_404(Car, id=self.kwargs["pk"])
        if car.owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect("cars:car-detail", pk=kwargs["pk"])


@login_required
def add_comment(request, pk):
    car = get_object_or_404(Car, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.car = car
        comment.save()
    return redirect("cars:car-detail", pk=pk)
