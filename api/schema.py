import typing
from datetime import date

import strawberry
from strawberry.types import Info

from repository import models


@strawberry.type
class CampaignDocumentType:

    id: int

    reference: str

    paper_type: str

    paper_creation_year: date

    location_origin: str

    latitude: float

    longitude: float

    paper_repetition: int

    crop_variety: str

    humidity_percentage_stat: int

    performance_stat: int

    relative_performance_stat: int

    grain_count_crop_stat: int

    grain_count_per_spike_stat: int

    weight_per_thousand_grains_stat: int

    proteins_percentage_stat: int

    ph_stat: int


@strawberry.type
class PreflightVarietyGroupType: ...


@strawberry.type
class VarietyGroupType: ...


@strawberry.type
class CampaignQueryType:

    @strawberry.field
    def document(self, info: Info) -> typing.List[CampaignDocumentType]:
        campaign_document_queryset = [
            CampaignDocumentType(
                id=entry.id,
                reference=entry.reference,
                paper_type=entry.paper_type,
                paper_creation_year=entry.paper_creation_year,
                location_origin=entry.location_origing,
                latitude=entry.latitude,  # type: ignore
                longitude=entry.longitude,  # type: ignore
                paper_repetition=entry.paper_repetition,
                crop_variety=entry.crop_variety,
                humidity_percentage_stat=entry.humidity_percentage_stat,  # type: ignore
                performance_stat=entry.performance_stat,  # type: ignore
                relative_performance_stat=entry.relative_performance_stat,  # type: ignore
                grain_count_crop_stat=entry.grain_count_crop_stat,
                grain_count_per_spike_stat=entry.grain_count_per_spike_stat,
                weight_per_thousand_grains_stat=entry.weight_per_thousand_grains_stat,  # type: ignore
                proteins_percentage_stat=entry.proteins_percentage_stat,  # type: ignore
                ph_stat=entry.ph_stat,  # type: ignore
            )
            for entry in models.CampaignDocumentsModel.objects.all()
        ]

        return campaign_document_queryset


STRAWBERRY_SCHEMA = strawberry.Schema(
    query=CampaignQueryType,
)
