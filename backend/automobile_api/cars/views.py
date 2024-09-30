from cars.forms import CarForm, CommentForm
from cars.models import Car, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class HomepageListView(ListView):
    """
    Displays a list of all cars on the homepage.

    Inherits:
        ListView: Generic view for displaying a list of objects.

    Attributes:
        template_name (str): The template used for rendering the homepage.

    Methods:
        get_queryset: Returns the queryset of cars with their related owners.
    """
    template_name = "cars/index.html"

    def get_queryset(self):
        """
        Retrieves all cars and prefetches related 'owner'
        information to optimize queries.

        Returns:
            QuerySet: A queryset of cars with related 'owner' instances.
        """
        queryset = (
            Car.objects.all()
            .select_related('owner')
        )
        return queryset


def car_detail(request, pk):
    """
    Displays the detail page of a specific car, along with its comments.

    Args:
        request: The HTTP request object.
        pk: The primary key of the car to be retrieved.

    Returns:
        HttpResponse: The rendered detail page for the specified car.
    """
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
    """
    Allows authenticated users to create a new car entry.

    Inherits:
        LoginRequiredMixin: Ensures the user is logged in
        before accessing this view.
        CreateView: Generic view for creating an object.

    Attributes:
        model (Car): The car model to be created.
        form_class (CarForm): The form class used to create a car.
        template_name (str): The template used for rendering
        he car creation page.

    Methods:
        get_success_url: Returns the URL to redirect to after
        successful car creation.
        form_valid: Automatically assigns the current user as
        the car's owner before saving.
    """
    model = Car
    form_class = CarForm
    template_name = "cars/create.html"

    def get_success_url(self):
        """
        Defines the URL to redirect to after a successful form submission.

        Returns:
            str: The URL for the car index page.
        """
        return reverse_lazy("cars:index")

    def form_valid(self, form):
        """
        Ensures the owner of the car is set to the current user before saving.

        Args:
            form: The submitted form instance.

        Returns:
            HttpResponse: The response from the parent class
            after the form is validated.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CarUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing car. Only the owner of the car can update it.

    Inherits:
        LoginRequiredMixin: Ensures that the user is authenticated.
        UpdateView: Generic view for updating an object.

    Attributes:
        model (Car): The car model to be updated.
        form_class (CarForm): The form class used for updating the car.
        template_name (str): The template used for
        rendering the car update page.
        success_url (str): The URL to redirect to after
        successfully updating the car.

    Methods:
        dispatch: Ensures that only the owner of the car or an authenticated
        user can update the car.
    """
    model = Car
    form_class = CarForm
    template_name = "cars/create.html"
    success_url = reverse_lazy("cars:index")

    def dispatch(self, request, *args, **kwargs):
        """
        Verifies that the user is authenticated and is the owner of the car.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments,
            including the car's primary key.

        Returns:
            HttpResponse: Redirects to the car detail page if the user is not
            authenticated  or if the user is not the car owner.
            Otherwise, proceeds with the request.
        """
        car = get_object_or_404(Car, pk=kwargs["pk"])
        if not request.user.is_authenticated:
            return redirect("cars:car-detail", pk=kwargs["pk"])
        if request.user != car.owner:
            return redirect("cars:car-detail", pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)


class CarDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting an existing car. Only the owner
    or a superuser can delete it.

    Inherits:
        LoginRequiredMixin: Ensures that the user is authenticated.
        DeleteView: Generic view for deleting an object.

    Attributes:
        model (Car): The car model to be deleted.
        template_name (str): The template used for rendering
        the car deletion confirmation page.
        success_url (str): The URL to redirect to after
        successfully deleting the car.

    Methods:
        get_context_data: Adds form data to the context for rendering.
        dispatch:
        Ensures that only the owner or a superuser can delete the car.
    """
    model = Car
    template_name = "cars/delete.html"
    success_url = reverse_lazy("cars:index")

    def get_context_data(self, **kwargs):
        """
        Adds the form class to the context for
        rendering the car deletion confirmation.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The updated context data containing the form class.
        """
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context

    def dispatch(self, request, *args, **kwargs):
        """
        Verifies that the user is the owner of the car or a
        superuser before allowing deletion.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments,
            including the car's primary key.

        Returns:
            HttpResponse: Redirects to the car detail page if
            the user is not the owner or a superuser.
            Otherwise, proceeds with the request to delete the car.
        """
        car = get_object_or_404(Car, id=self.kwargs["pk"])
        if car.owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect("cars:car-detail", pk=kwargs["pk"])


@login_required
def add_comment(request, pk):
    """
    Handles adding a comment to a specific car.
    Only authenticated users can add comments.

    Args:
        request: The HTTP request object containing the comment data.
        pk: The primary key of the car to which the comment is being added.

    Returns:
        HttpResponse: Redirects back to the car detail page after
        the comment is successfully added.
    """
    car = get_object_or_404(Car, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.car = car
        comment.save()
    return redirect("cars:car-detail", pk=pk)
