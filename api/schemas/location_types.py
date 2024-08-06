import strawberry


@strawberry.type(
    description="Represents a minimal set of information of a crop variety entry"
)
class LocationOptionsType:
    """
    Represents a minimal set of information of a location entry
    """

    id: int

    region_name: str
