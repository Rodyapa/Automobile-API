from django.contrib.admin import ModelAdmin, register, site, StackedInline
from cars.models import Car, Comment
from django.contrib.auth.models import Group

site.unregister(Group)
site.site_header = "Automobile Portal Admin zone"


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = (
        "car",
        "author",
        "content"
    )


class CommentInlineModel(StackedInline):
    model = Comment
    extra = 1


@register(Car)
class CarAdmin(ModelAdmin):
    search_fields = ("make", "model", "year", "owner")
    list_filter = ("make", "model", "year", "owner")
    list_display = ("make", "model", "year", "owner")
    inlines = (CommentInlineModel, )
