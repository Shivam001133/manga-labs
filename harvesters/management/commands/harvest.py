from django.core.management.base import BaseCommand
from harvesters.models import Harvester, HarvestType
from pathlib import Path
import logging
import json

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create entry web data in db"

    def read_json(self):
        try:
            with Path.open("domain_index.json") as file:  # ruff:noqa:UP015
                return json.load(file)
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format in file!"))
            return None

    def get_harvest_type(self, harvest_type):
        if harvest_type == "manga":
            return HarvestType.MANGA
        if harvest_type == "anime":
            return HarvestType.ANIME
        return HarvestType.NONE

    def save_to_db(self):
        data = self.read_json()
        mangas = data.get("mangas", [])

        save_data = [
            Harvester(
                domain_name=manga.get("domain_name"),
                domain_url=manga.get("domain_url"),
                harvest_type=self.get_harvest_type(manga.get("harvest_type")),
                is_active=(manga.get("is_active", "true") == "true"),
            )
            for manga in mangas
        ]

        Harvester.objects.bulk_create(save_data)

    def handle(self, *args, **kwargs):
        logger.info("Start creating web data in db")
        self.save_to_db()
        logger.info("End creating web data in db")
