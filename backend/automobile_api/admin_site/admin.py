from cars.models import Car, Comment
from django.contrib.admin import ModelAdmin, StackedInline, register, site
from django.contrib.auth.models import Group

site.unregister(Group)
site.site_header = "Automobile Portal Admin zone"


@register(Comment)
class CommentAdmin(ModelAdmin):
    """
    Custom admin panel configuration for the Comment model.

    Attributes:
        list_display (tuple): Fields to display in the list view
        of the Comment model.
    """
    list_display = (
        "car",
        "author",
        "content"
    )


class CommentInlineModel(StackedInline):
    """
    Inline model configuration for displaying comments
    within the Car admin page.

    Attributes:
        model (Comment): The model to display inline.
        extra (int): Number of extra empty comment forms
        to display in the admin page.
    """
    model = Comment
    extra = 1


@register(Car)
class CarAdmin(ModelAdmin):
    """
    Custom admin panel configuration for the Car model.

    Attributes:
        search_fields (tuple): Fields that can be searched in the admin panel.
        list_filter (tuple): Fields by which admin users can filter results.
        list_display (tuple): Fields to display
        in the list view of the Car model.
        inlines (tuple): Inline model(s) to display alongside
        the Car model (in this case, comments).
    """
    search_fields = ("make", "model", "year", "owner")
    list_filter = ("make", "model", "year", "owner")
    list_display = ("make", "model", "year", "owner")
    inlines = (CommentInlineModel, )
