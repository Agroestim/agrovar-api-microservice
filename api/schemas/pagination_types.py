import typing

import strawberry


@strawberry.type(
    description="Represents the metadata required to perform a further query with additional data of the same type.",
)
class PaginationMetaType:
    """
    Represents the metadata required to perform a further query with additional data of the same type.
    """

    next_cursor: typing.Optional[str]
