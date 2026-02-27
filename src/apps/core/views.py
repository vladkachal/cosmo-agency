from django.views.generic import TemplateView

from apps.slider.models import SliderItem


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["slides"] = (
            SliderItem.objects.active()
            .select_related("image")
            .only(
                "name",
                "image__file",
                # The next fields are not used directly in the template,
                # but are required internally by django-filer
                # to fully initialize the Image instance without extra db queries.
                "image__sha1",
                "image__is_public",
                "image___file_size",
            )
        )
        return context
