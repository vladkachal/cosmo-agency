import logging

from pathlib import Path
from typing import TYPE_CHECKING, Any

from filer.management.commands.import_files import FileImporter

from django.core.management import BaseCommand, CommandParser
from django.db import transaction

from ...models import SliderItem

if TYPE_CHECKING:
    from filer.models import File, Folder, Image

    from django.core.files import File as DjangoFile

logger = logging.getLogger(__name__)


class CustomFileImporter(FileImporter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the CustomFileImporter instance.

        :param args: Positional arguments for initialization.
        :param kwargs: Keyword arguments for initialization. Inherits 'path',
            'base_folder', and 'verbosity' from FileImporter.
        """
        super().__init__(*args, **kwargs)
        self.imported_objects: list[File | Image] = []

    def import_file(self, file_obj: "DjangoFile", folder: "Folder") -> "File | Image":
        """
        Override the import_file method to store created objects in a list.

        :param file_obj: The file object to import.
        :param folder: The Folder instance where the file should be stored.
        :return: The created File or Image object.
        """
        obj = super().import_file(file_obj, folder)
        self.imported_objects.append(obj)  # Save the created object in the list
        return obj

    def get_imported_objects(self) -> list["File | Image"]:
        """
        Retrieve the list of all imported File and Image objects.

        :return: A list of File or Image objects that were created.
        """
        return self.imported_objects


class Command(BaseCommand):
    """
    Management command for importing slider images and creating SliderItem objects.

    Examples:
        manage.py import_slides --path=/path/to/slides --folder="Slider: Преимущества"

    The command:
        1. Imports files into django-filer
        2. Creates SliderItem objects based on imported images
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--path",
            action="store",
            dest="path",
            required=True,
            help="Import files located in the path",
        )

        parser.add_argument(
            "--folder",
            action="store",
            dest="base_folder",
            default=False,
            help=(
                "Specify the destination folder in which the directory structure"
                " should be imported"
            ),
        )

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        logger.info("Starting slider import process.")

        raw_path = Path(options["path"])
        path = Path(raw_path)
        if not path.exists() or not path.is_dir():
            logger.error("Provided path does not exist: %s", raw_path)
            return

        base_folder = options["base_folder"]
        logger.info("Importing images from '%s' into folder '%s'.", path, base_folder)

        filer_importer = CustomFileImporter(path=raw_path, base_folder=base_folder)
        filer_importer.walker()
        filer_images = filer_importer.get_imported_objects()
        if not filer_images:
            logger.warning("No images were imported from %s.", path)
            return

        slider_items = SliderItem.objects.create_slider_items(filer_images)
        logger.info(
            "Successfully created %d slider items in folder '%s'.",
            len(slider_items),
            base_folder,
        )
