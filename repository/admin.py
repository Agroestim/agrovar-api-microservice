from django.contrib import admin

from repository import models


# Register your models here.
@admin.register(models.CampaignDocumentsModel)
class CampaignDocumentsAdmin(admin.ModelAdmin):
    # Filter by paper_creation
    list_filter = ["paper_creation_year"]


@admin.register(models.VarietyOptionsModel)
class VarietyOptionsAdmin(admin.ModelAdmin):
    # Filter by variety_name
    list_filter = ["variant_name"]


@admin.register(models.LocationOptionsModel)
class LocationOptionsAdmin(admin.ModelAdmin):
    # Filter by region_name
    list_filter = ["region_name"]
