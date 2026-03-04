import logging

from pathlib import Path
from typing import TYPE_CHECKING

from easy_thumbnails.models import Thumbnail

from django.db import models
from django.db.models import OuterRef, Subquery

if TYPE_CHECKING:
    from filer.models import File as FilerFile, Image as FilerImage

    from .models import SliderItem

logger = logging.getLogger(__name__)


class SliderItemQuerySet(models.QuerySet["SliderItem"]):
    def active(self) -> "SliderItemQuerySet":
        return self.filter(is_active=True)


class SliderItemManager(models.Manager["SliderItem"]):
    @staticmethod
    def build_thumbnail_subquery(size: str) -> "Subquery":
        return Subquery(
            Thumbnail.objects.filter(
                source__id=OuterRef("image__file_ptr_id"),
                name__contains=f"__{size}_",
                modified__gte=OuterRef("image__modified_at"),
            )
            .order_by("-modified")
            .values_list("name")[:1]
        )

    @staticmethod
    def create_slider_items(
        filer_images: list["FilerFile | FilerImage"],
    ) -> list["SliderItem"]:
        """
        Create SliderItem instances from FilerImage instances.

        :param filer_images: List of FilerFile or FilerImage instances
        :return: List of created SliderItem instances
        """
        from .models import SliderItem

        slider_items = [
            SliderItem(
                name=Path(img.original_filename).stem,
                image=img,
                order=img.id,
                is_active=True,
            )
            for img in filer_images
        ]

        SliderItem.objects.bulk_create(slider_items)
        logger.info("Successfully created %d SliderItem instances.", len(slider_items))

        return slider_items


SliderItemManager = SliderItemManager.from_queryset(SliderItemQuerySet)
