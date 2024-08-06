import enum
import typing
from datetime import date

import strawberry
from strawberry import types

from api.pagination import resolve_cursor
from api.schemas.campaign_types import CampaignDocumentType
from api.schemas.location_types import LocationOptionsType
from api.schemas.pagination_types import PaginationMetaType
from api.schemas.variety_types import VarietyOptionsType
from repository import models

# Query field resolvers


def resolve_campaign_document(
    self, info: types.Info, limit: int, cursor: str
) -> "PaginatedCampaignDocumentType":

    sliced_campaign_documents, next_cursor = resolve_cursor(
        search_limit=limit, encoded_cursor=cursor, model=models.CampaignDocumentsModel
    )

    paginated_entries = [
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
        for entry in sliced_campaign_documents
    ]

    return PaginatedCampaignDocumentType(
        entries=paginated_entries,
        page_meta=PaginationMetaType(next_cursor=next_cursor),
    )


def resolve_variety_options(
    self, info: types.Info, limit: int, cursor: str
) -> "PaginatedVarietyOptionsType":

    sliced_variety_options, next_cursor = resolve_cursor(
        search_limit=limit, encoded_cursor=cursor, model=models.VarietyOptionsModel
    )

    paginated_entries = [
        VarietyOptionsType(
            id=entry.id,
            tradename=entry.tradename,
            variant_name=entry.variant_name,
        )
        for entry in sliced_variety_options
    ]

    return PaginatedVarietyOptionsType(
        options=paginated_entries, page_meta=PaginationMetaType(next_cursor=next_cursor)
    )


def resolve_location_options(
    self, info: types.Info, limit: int, cursor: str
) -> "PaginatedLocationOptionsType":

    sliced_locations, next_cursor = resolve_cursor(
        search_limit=limit, encoded_cursor=cursor, model=models.LocationOptionsModel
    )

    paginated_entries = [
        LocationOptionsType(
            id=entry.id,
            region_name=entry.region_name,
        )
        for entry in sliced_locations
    ]

    return PaginatedLocationOptionsType(
        options=paginated_entries, page_meta=PaginationMetaType(next_cursor=next_cursor)
    )


def resolve_campaign_document_option(
    self, info: types.Info, limit: int, cursor: str
) -> "PaginatedCampaignDocumentOptionsType":

    sliced_campaign_documents, next_cursor = resolve_cursor(
        search_limit=limit, encoded_cursor=cursor, model=models.CampaignDocumentsModel
    )

    paginated_entries = [
        CampaignDocumentOptionType(
            id=entry.id,
            reference=entry.reference,
            location_origin=entry.location_origin.region_name,
            date_origin=entry.paper_creation_year,
            crop_variant=entry.crop_variety.variant_name,
        )
        for entry in sliced_campaign_documents
    ]

    return PaginatedCampaignDocumentOptionsType(
        options=paginated_entries,
        page_meta=PaginationMetaType(next_cursor=next_cursor),
    )


def resolve_preflight_options(self, info: types.Info) -> "PreflightOptionsType":
    return PreflightOptionsType()


@strawberry.type(
    description="Represents a wrapper for the CampaignDocumentOptionsType query with the pagination metadata."
)
class PaginatedCampaignDocumentOptionsType:
    """
    Represents the pagination wrapper that provides the required data for manage the pagination of the queries.
    """

    options: typing.List["CampaignDocumentOptionType"]

    page_meta: typing.Optional[PaginationMetaType]


@strawberry.type(
    description="Represents a wrapper for the LocationOptionsType query with the pagination metadata.",
)
class PaginatedLocationOptionsType:
    """
    Represents the pagination wrapper that provides the required data for manage the pagination of the queries.
    """

    options: typing.List["LocationOptionsType"]

    page_meta: typing.Optional[PaginationMetaType]


@strawberry.type(
    description="Represents a wrapper for the VarietyOptionsType query with the pagination metadata.",
)
class PaginatedVarietyOptionsType:
    """
    Represents twhe pagination wrapper that provides the required data for manage the pagination of the queries.
    """

    options: typing.List["VarietyOptionsType"]

    page_meta: typing.Optional[PaginationMetaType]


@strawberry.type(
    description="Represents a wrapper for the CampaignDocumentType query with the pagination metadata.",
)
class PaginatedCampaignDocumentType:
    """
    Represents the pagination wrapper that provides the required data for manage the pagination of the queries.
    """

    entries: typing.List[CampaignDocumentType]

    page_meta: typing.Optional[PaginationMetaType]


@strawberry.type(
    description="Represents a minimal set of information of a crop variety entry"
)
class CampaignDocumentOptionType:
    """
    Represents a minimal set of information of a campaign document entry
    """

    id: int

    reference: str

    location_origin: str

    date_origin: date

    crop_variant: str


# Composite preflight query types


@strawberry.type(description="")
class PreflightOptionsType:
    """
    Represents a set of options that are required to preload the application options.
    Like a form entry option or a user language preference.
    """

    variety_options: PaginatedVarietyOptionsType = strawberry.field(
        resolver=resolve_variety_options,
        description="Resolves the variety preflight options",
    )

    location_options: PaginatedLocationOptionsType = strawberry.field(
        resolver=resolve_location_options,
        description="Resolves the location preflight options",
    )

    campaign_options: PaginatedCampaignDocumentOptionsType = strawberry.field(
        resolver=resolve_campaign_document_option,
        description="Resolves the campaign document preflight options",
    )


@strawberry.type(
    description="This type is a set of all the available queries in this API version."
)
class MixedType:

    campaign_documents: PaginatedCampaignDocumentType = strawberry.field(
        resolver=resolve_campaign_document,
    )

    preflight_options: PreflightOptionsType = strawberry.field(
        resolver=resolve_preflight_options,
    )


# Mutation types

# Graphql Schema

STRAWBERRY_SCHEMA = strawberry.Schema(
    query=MixedType,
)
