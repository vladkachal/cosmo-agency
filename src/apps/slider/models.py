from filer.fields.image import FilerImageField

from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import SliderItemManager


class SliderItem(models.Model):
    name = models.CharField(_("name"), max_length=255)
    image = FilerImageField(
        verbose_name=_("image"),
        on_delete=models.CASCADE,
        related_name="slider_item",
    )
    order = models.PositiveIntegerField(_("order"), default=0, db_index=True)
    is_active = models.BooleanField(_("is active"), default=True)

    objects = SliderItemManager()

    class Meta:
        verbose_name = _("slide")
        verbose_name_plural = _("slides")
        ordering = ("order",)

    def __str__(self) -> str:
        return self.name
