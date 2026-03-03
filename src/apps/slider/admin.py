from typing import TYPE_CHECKING

from adminsortable2.admin import SortableAdminMixin

from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import SliderItem

if TYPE_CHECKING:
    from .managers import SliderItemQuerySet


@admin.register(SliderItem)
class SliderItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("preview", "name", "is_active")
    list_display_links = ("name",)
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name",)

    def get_queryset(self, request: HttpRequest) -> "SliderItemQuerySet":
        return super().get_queryset(request).select_related("image")

    @admin.display(description=_("preview"))
    def preview(self, obj: SliderItem) -> str:
        if obj.image:
            return format_html(
                '<a href="{url}" target="_blank">'
                '<img src="{url}" style="height:100px; cursor:pointer;" />'
                "</a>",
                url=obj.image.url,
            )
        return "-"
