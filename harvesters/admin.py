from django.contrib import admin
from harvesters.models import Harvester, ScrapingHarvest


@admin.register(Harvester)
class HarvesterAdmin(admin.ModelAdmin):
    list_display = (
        "domain_name",
        "harvest_type",
        "is_active",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_filter = (
        "harvest_type",
        "is_active",
    )


@admin.register(ScrapingHarvest)
class ScrapingHarvestAdmin(admin.ModelAdmin):
    list_display = ("harvest", "next_scrape", "last_scrape", "is_active")
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_filter = (
        "harvest",
        "is_active",
    )
