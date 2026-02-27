import logging

from django.db import models

logger = logging.getLogger(__name__)


class SliderItemQuerySet(models.QuerySet["SliderItem"]):
    def active(self) -> "SliderItemQuerySet":
        return self.filter(is_active=True)


class SliderItemManager(models.Manager["SliderItem"]): ...


SliderItemManager = SliderItemManager.from_queryset(SliderItemQuerySet)
