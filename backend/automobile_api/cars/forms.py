from django import forms
from cars.models import Comment, Car


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", )


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ("owner", "created_at", "updated_at")
