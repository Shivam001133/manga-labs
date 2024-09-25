from django.contrib import admin
from mangavault.models import MangaVault


@admin.register(MangaVault)
class MangaVaultAdmin(admin.ModelAdmin):
    list_display = ("title", "website", "is_active", "updated_at")
    readonly_fields = ("updated_at", "created_at")
    list_filter = ("is_active",)
