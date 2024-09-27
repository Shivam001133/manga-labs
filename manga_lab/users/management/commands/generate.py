from django.core.management.base import BaseCommand
# , CommandError
from mangavault.models import MangaGenre
from harvesters.models import HarvestType
import requests
import json


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
            for model_obj in data:
                try:
                    MangaGenre.objects.create(model_obj)
                except Exception as e:  # noqa:BLE001
                    print("***********", e)  # noqa:T201
                    continue
        self.style.SUCCESS("Genre created successful")

    def generate_genres(self, user_choice: str) -> None:
        base_url = "https://api.jikan.moe/v4/genres/"
        endpoint = ["m", "manga", "a", "anime"]
        res_data = []
        user_choice_none = user_choice is None
        if user_choice in endpoint or user_choice_none:
            if user_choice[0] == endpoint[0] or user_choice_none:
                res_data.append(self.send_request(url=base_url + "manga"))
                if user_choice_none:
                    res_data.append(self.send_request(url=base_url + "anime"))
            else:
                res_data.append(self.send_request(url=base_url + "anime"))
        else:
            self.style.WARNING(f"Please chose one of these option {endpoint}")

        for info in res_data:
            genre_data = info["data"][0]
            r_t = [c_h for c_h in HarvestType if c_h._value_[0] == user_choice[0]]
            if len(res_data) > 1 and info is res_data[-1]:
                self.create_genre_entry(
                    {
                        "title": genre_data["name"],
                        "description": "",
                        "related_to": r_t[0],
                        "is_active": True,
                    }
                )
            elif r_t[0]._value_ in set("both", "manga"):
                self.create_genre_entry(
                    MangaGenre(
                        title=genre_data["name"],
                        description="",
                        related_to=HarvestType.MANGA,
                        is_active=True,
                    ),
                    bulk=True,
                )
            else:
                self.create_genre_entry(
                    MangaGenre(
                        title=genre_data["name"],
                        description="",
                        related_to=r_t[0],
                        is_active=True,
                    ),
                    bulk=True,
                )

    def handle(self, *args, **options):
        self.generate_genres(options.get("genre"))
        self.style.SUCCESS("generate command completed :)")
