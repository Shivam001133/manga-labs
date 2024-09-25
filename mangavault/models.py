from django.utils.translation import gettext_lazy as _
from harvesters.models import Harvester
from django.db import models


class MangaCategory(models.TextChoices):
    MANGA = "Manga", _("Manga")
    MANHWA = "Manhwa", _("Manhwa")
    MANHUA = "Manhua", _("Manhua")
    COMICS = "Comics", _("Comics")
    NONE = "none", _("Comics")


class MangaVault(models.Model):
    title = models.CharField(max_length=100)
    website = models.ForeignKey(Harvester, on_delete=models.RESTRICT)
    cover_img = models.URLField()
    description = models.TextField()
    vault_url = models.URLField()
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self
