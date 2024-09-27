from django.db import models
from django.utils.translation import gettext_lazy as _


class HarvestType(models.TextChoices):
    MANGA = "manga", _("Manga")
    ANIME = "anime", _("Anime")
    BOTH = "both", _("Both")
    NONE = "none", _("None")


class Harvester(models.Model):
    domain_name = models.CharField(max_length=25)
    domain_url = models.URLField()
    harvest_type = models.CharField(
        max_length=15,
        choices=HarvestType.choices,
        default=HarvestType.NONE,
    )
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.domain_name


class ScrapingHarvest(models.Model):
    harvest = models.OneToOneField(Harvester, on_delete=models.SET_NULL, null=True)
    next_scrape = models.DateTimeField()
    last_scrape = models.DateField(null=True)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.harvest.domain_name
