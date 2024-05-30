import typing
from datetime import date

import strawberry
from strawberry.types import Info

from repository import models

# Query Resolvers


def resolve_campaign_document(
    self, info: Info, offset: int, limit: int
) -> typing.List["CampaignDocumentType"]:
    return [
        CampaignDocumentType(
            id=entry.id,
            reference=entry.reference,
            paper_type=entry.paper_type,
            paper_repetition=entry.paper_repetition,
            paper_creation_year=entry.paper_creation_year,
            location_origin=entry.location_origin.region_name,
            latitude=entry.latitude,  # type: ignore
            longitude=entry.longitude,  # type: ignore
            crop_variety=entry.crop_variety.variant_name,
            humidity_percentage_stat=entry.humidity_percentage_stat,  # type: ignore
            performance_stat=entry.performance_stat,  # type: ignore
            relative_performance_stat=entry.relative_performance_stat,  # type: ignore
            grain_count_crop_stat=entry.grain_count_crop_stat,
            grain_count_per_spike_stat=entry.grain_count_per_spike_stat,
            weight_per_thousand_grains_stat=entry.weight_per_thousand_grains_stat,  # type: ignore
            proteins_percentage_stat=entry.proteins_percentage_stat,  # type: ignore
            ph_stat=entry.ph_stat,  # type: ignore
        )
        for entry in models.CampaignDocumentsModel.objects.all()[:offset:limit]
    ]


def resolve_variety_options(self, info: Info) -> typing.List["VarietyOptionsType"]:
    return [
        VarietyOptionsType(
            id=entry.id,
            tradename=entry.tradename,
            variant_name=entry.variant_name,
        )
        for entry in models.VarietyOptionsModel.objects.all()
    ]


def resolve_location_options(self, info: Info) -> typing.List["LocationOptionsType"]:
    return [
        LocationOptionsType(
            id=entry.id,
            region_name=entry.region_name,
        )
        for entry in models.LocationOptionsModel.objects.all()
    ]


def resolve_campaign_document_option(
    self, info: Info, offset: int, limit: int
) -> typing.List["CampaignDocumentOptionType"]:
    return [
        CampaignDocumentOptionType(
            id=entry.id,
            reference=entry.reference,
            location_origin=entry.location_origin.region_name,
            date_origin=entry.paper_creation_year,
            crop_variant=entry.crop_variety.variant_name,
        )
        for entry in models.CampaignDocumentsModel.objects.all()[:offset:limit]
    ]


# Strawberry Types


@strawberry.type(
    description="Represents a campaign document where stores all the crop information"
)
class CampaignDocumentType:
    """
    Represents a campaign document where stores all the crop information.
    """

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


@strawberry.type(description="Represents a crop variety")
class VarietyOptionsType:
    """
    Represents a crop variety.
    """

    id: int

    tradename: str

    variant_name: str


@strawberry.type(
    description="Represents a location such a city where the campaign was documented"
)
class LocationOptionsType:
    """
    Represents a location such a city where the campaign was documented.
    """

    id: int

    region_name: str


@strawberry.type(description="Represents a campaign document")
class CampaignDocumentOptionType:
    """
    Represents a campaign document type used for get the preflight data required by the frontend
    """

    id: int

    reference: str

    location_origin: str

    date_origin: date

    crop_variant: str


@strawberry.type(
    description="Represents a mixed query used for get the preflight data required by the frontend"
)
class PreflightOptionsType:
    """
    Represents a mixed query used for get the preflight data required by the frontend.
    """

    variety_options: typing.List[VarietyOptionsType] = strawberry.field(
        resolver=resolve_variety_options,
        description="Make a preflight query that resolve the crop variety options.",
    )

    location_options: typing.List[LocationOptionsType] = strawberry.field(
        resolver=resolve_location_options,
        description="Make a preflight query that resolve the campaing location options.",
    )

    campaign_options: typing.List[CampaignDocumentOptionType] = strawberry.field(
        resolver=resolve_campaign_document_option,
        description="Make a preflight query that resolves the campaign document options.",
    )


@strawberry.type(
    description="Represents a final mixed type that contains all of the possible operations available"
)
class MixedType:
    """
    Represents a final mixed type that contains all of the possible operations available.
    """

    campaign_documents: typing.List[CampaignDocumentType] = strawberry.field(
        resolver=resolve_campaign_document,
        description="asdasdasdasdasdasdasasd",
    )

    @strawberry.field(description="asdasdasdasd")
    def preflight_options(self, info: Info) -> PreflightOptionsType:
        return PreflightOptionsType()


STRAWBERRY_SCHEMA = strawberry.Schema(
    query=MixedType,
)
