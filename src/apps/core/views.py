from django.views.generic import TemplateView

from apps.slider.models import SliderItem


class IndexView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        # TODO:
        #   - Move hardcoded thumbnail options (size) to THUMBNAIL_ALIASES variable
        #   to avoid duplication across the codebase.
        #   - Generate thumbnails on slide image upload.
        context["slides"] = (
            SliderItem.objects.active()
            .select_related("image")
            .annotate(
                thumb_nav_sm=SliderItem.objects.build_thumbnail_subquery("146x146"),
                thumb_nav_md=SliderItem.objects.build_thumbnail_subquery("210x210"),
            )
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
