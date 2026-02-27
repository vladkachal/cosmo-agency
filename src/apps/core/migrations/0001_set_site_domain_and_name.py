from django.conf import settings
from django.db import migrations


def update_site_forward(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            "domain": "your-domain",
            "name": "CosmoAgency",
        },
    )


def update_site_backward(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            "domain": "example",
            "name": "Example",
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
