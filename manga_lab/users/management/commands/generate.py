from django.core.management.base import BaseCommand

# , CommandError
from django.db.utils import IntegrityError
from mangavault.models import MangaGenre
from harvesters.models import HarvestType
import requests
import json
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument(
            "--genre",
            "-g",
            dest="genre",
            type=str,
            default="both",  # anime, manga
            help="Create entry in MangaGenre table",
        )

    def send_request(self, url: str) -> dict:
        response = requests.get(url=url, timeout=30)
        success_res = 200
        if response.status_code == success_res:
            return json.loads((response.content).decode("utf8"))
        return None

    def create_genre_entry(self, data: list, bulk: bool = False) -> None:  # noqa:FBT001 FBT002
        if bulk:
            MangaGenre.objects.bulk_create(data)
        else:
            try:
                genre = MangaGenre.objects.get(title=data["title"])
                if genre.related_to == data["related_to"]:
                    genre.related_to = HarvestType.BOTH
            except IntegrityError:
                MangaGenre.objects.create(**data)
        logger.info("Genre created successful")

    def generate_genres(self, user_choice: str) -> None:
        base_url = "https://api.jikan.moe/v4/genres/"
        endpoint = ["m", "manga", "a", "anime"]
        res_data = []
        user_choice_none = user_choice == "both"
        if user_choice in endpoint or user_choice_none:
            if user_choice[0] == endpoint[0] or user_choice_none:
                res_data.append(self.send_request(url=base_url + "manga"))
                if user_choice_none:
                    res_data.append(self.send_request(url=base_url + "anime"))
            else:
                res_data.append(self.send_request(url=base_url + "anime"))
        else:
            warning_mess = f"Please chose one of these option {endpoint}"
            logger.warning(warning_mess)

        for info in res_data:
            genre_data = info["data"]
            bulk_data = []
            r_t = [c_h for c_h in HarvestType if c_h._value_[0] == user_choice[0]]
            for genre in genre_data:
                if len(res_data) > 1 and info is res_data[-1]:
                    self.create_genre_entry(
                        data={
                            "title": genre["name"],
                            "description": "",
                            "related_to": r_t[0],
                            "is_active": True,
                        }
                    )
                elif r_t[0]._value_ in set({"both", "manga"}):
                    bulk_data.append(
                        MangaGenre(
                            title=genre["name"],
                            description="",
                            related_to=HarvestType.MANGA,
                            is_active=True,
                        )
                    )
                else:
                    bulk_data.append(
                        MangaGenre(
                            title=genre["name"],
                            description="",
                            related_to=r_t[0],
                            is_active=True,
                        )
                    )
            if bulk_data:
                self.create_genre_entry(bulk_data, bulk=True)

    def handle(self, *args, **options):
        self.generate_genres(options.get("genre"))
        logger.info("generate command completed :)")
