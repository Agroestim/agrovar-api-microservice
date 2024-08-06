import strawberry


@strawberry.type(
    description="Represents a minimal set of information of a crop variety entry"
)
class VarietyOptionsType:
    """
    Represents a minimal set of information a crop variety entry
    """

    id: int

    tradename: str

    variant_name: str
