from django.contrib import admin

from repository import models


# Register your models here.
@admin.register(models.CampaignDocumentsModel)
class CampaignDocumentsAdmin(admin.ModelAdmin):
    # Filter by paper_creation
    list_filter = ["paper_creation_year"]


@admin.register(models.VarietyOptionsModel)
class VarietyOptionsAdmin(admin.ModelAdmin): ...
