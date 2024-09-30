from cars.models import Car, Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    A form for creating and updating comments on a car.

    Inherits:
        forms.ModelForm: Standard Django form for
        creating and editing model instances.

    Meta:
        model (Comment): The model that the form is associated with.
        fields (tuple): A tuple specifying the fields to include in the form
        ('content' in this case).
    """
    class Meta:
        model = Comment
        fields = ("content",)


class CarForm(forms.ModelForm):
    """
    A form for creating and updating car instances, excluding fields
    that are automatically managed.

    Inherits:
        forms.ModelForm: Standard Django form for creating and editing model
        instances.

    Meta:
        model (Car): The model that the form is associated with.
        exclude (tuple): A tuple specifying fields to exclude from the form
        ('owner', 'created_at', 'updated_at').
    """
    class Meta:
        model = Car
        exclude = ("owner", "created_at", "updated_at")
