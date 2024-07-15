import json
import typing
from base64 import b64decode, b64encode

from django.db import models

_ModelType = typing.TypeVar("_ModelType", bound=models.Model)


class Cursor(typing.TypedDict):
    id: int

    select_by_related_field: str | None


class Pagination:

    VALID_CURSOR_FIELDS = ["id", "select_by_related_field"]

    def check_valid_cursor(self, cursor: Cursor) -> bool:
        """Check if all the fields in the cursor dictionary are valid.

        Args:
            cursor (Cursor): A dictionary with the pagination metadata.

        Returns:
            bool: Returns True if all the dictionary fields are valid.
        """
        return all([field in self.VALID_CURSOR_FIELDS for field in cursor])

    def encode_cursor(self, cursor: Cursor) -> str:
        """Returns an encoded stringified cursor in base 64.

        Args:
            cursor (Cursor): A dictionary with the pagination metadata

        Returns:
            str: Returns a stringified dictionary in base 64.
        """
        if not self.check_valid_cursor(cursor):
            raise ValueError("The parameter 'cursor' is not a valid cursor dictionary.")

        serialized_json = json.dumps(cursor).encode("utf-8")
        encoded_cursor = b64encode(serialized_json).decode("utf-8")

        return encoded_cursor

    def decode_cursor(self, cursor: str) -> Cursor:
        """Returs a decoded cursor in a dictionary.

        Args:
            cursor (str): A stringified cursor in base 64.

        Returns:
            Cursor: A decoded cursor built with the deserilized string.
        """
        decoded_cursor = b64decode(cursor.encode("utf-8")).decode("utf-8")
        deserialized_json = json.loads(decoded_cursor)

        if not self.check_valid_cursor(deserialized_json):
            raise ValueError("The parameter 'cursor' is not a valid cursor dictionary.")

        return deserialized_json


def resolve_cursor(
    *, search_limit: int, encoded_cursor: str, model: typing.Type[_ModelType]
) -> tuple[list[_ModelType], str]:
    """This function is responsable of resolve the encoded cursor and return a list of
    specific entries.

    Args:
        search_limit (int): An integer number that limits the entries to serve.
        encoded_cursor (str): A cursor that is incoded in base 64.
        model (typing.Type[_ModelType]): A model to be queried.

    Returns:
        tuple[list[_ModelType], str]: A tuple with the queried entries and the next cursor.
    """

    if encoded_cursor == "":
        raise ValueError("Cannot provide a empty value for 'encoded_cursor' argument")

    pagination = Pagination()

    cursor = pagination.decode_cursor(encoded_cursor)

    # Retrives the cursor metadata.
    cursor_selection_filter_id = cursor["id"]
    cursor_select_by_related_field = cursor["select_by_related_field"]

    # Store in memory all entries selected.
    selected_entries: list[_ModelType] = []

    # If the 'cursor_select_by_related_field' attribute were not provided
    # then will search all entries greater than last entry id cursor.
    if cursor_select_by_related_field == "":
        selected_entries = [
            entry for entry in model.objects.filter(id__gte=cursor_selection_filter_id)
        ]
    # If the 'cursor_select_by_related_field' attribute were provided then
    # will search all entries related with the db field and any with an id
    # greater than last entry id cursor.
    else:
        selected_entries = [
            entry
            for entry in model.objects.select_related(
                cursor_select_by_related_field
            ).filter(id__gte=cursor_selection_filter_id)
        ]

    # Limit the query search using the selection limit.
    paginated_entries = selected_entries[: search_limit + 1]

    # Use the last entry as a cursor using its id as a reference.
    next_cursor_target = paginated_entries.pop(-1)
    next_cursor_target_with_id = next_cursor_target.id  # type: ignore

    # Encode the cursor.
    next_cursor = pagination.encode_cursor(
        {
            "id": next_cursor_target_with_id,
            "select_by_related_field": cursor_select_by_related_field,
        }
    )

    return paginated_entries, next_cursor
