from datetime import date

import strawberry


@strawberry.type(description="Represents a container for the campaign document.")
class CampaignDocumentType:
    """
    A campaign document is a paper that collects all the information about the certain crop and involved growth
    variables.
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
