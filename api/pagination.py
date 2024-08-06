import json
import typing
from base64 import b64decode, b64encode

from django.db import models

type ModelType = type[models.Model]


class Filters(typing.TypedDict):
    filter: str
    key: str
    value: typing.Any


class Cursor(typing.TypedDict):
    """Represents a pagination cursor."""

    id: int
    """Represents the next entry that cursor will target."""


class Pagination:

    CURSOR_FIELDS = ["id"]

    CURSOR_PREFIXES = ["select_related"]
    CURSOR_SUFFIXES = ["location_origin", "crop_variety"]

    @staticmethod
    def hash(cursor: str) -> str:
        """This method generate a hash with the given cursor that will
        be used to dynamicly cache all paginated queries.

        Args:
            cursor (str): A encoded cursor.

        Returns:
            str: A hash.
        """

        raise NotImplementedError("This method has not been implemented yet")

    @staticmethod
    def is_cached(hash: str) -> bool:
        """Check if the given hash has been cached.

        Args:
            hash (str): A hash.

        Returns:
            bool: True if the hash has been cached.
        """
        raise NotImplementedError("This method has not been implemented yet")

    @staticmethod
    def __is_field_filter(key: str) -> bool:
        """Check if the given key is a filter field of a cursor.

        Args:
            key (str): A key from a decoded cursor.

        Returns:
            bool: True if is a filter field.
        """
        field_namespace = key.split("__", 2)

        if len(field_namespace) == 1:
            return False

        field_prefix = field_namespace[0]
        field_suffix = field_namespace[1]

        return (
            field_prefix in Pagination.CURSOR_PREFIXES
            and field_suffix in Pagination.CURSOR_SUFFIXES
        )

    @staticmethod
    def __is_valid_field(key: str) -> bool:
        """Check if the given key is in the valid cursor keys list.

        Args:
            key (str): A cursor key.

        Returns:
            bool: True if the key is valid.
        """
        return (key == "" or key == " ") or key in Pagination.CURSOR_FIELDS

    @staticmethod
    def check_valid_cursor(cursor: Cursor) -> bool:
        """Check if all the fields in the cursor dictionary are valid.

        Args:
            cursor (Cursor): A dictionary with the pagination metadata.

        Returns:
            bool: Returns True if all the dictionary fields are valid.
        """

        # NOTE []: This validation process can be improve using a cache system.

        valid_keys = [
            Pagination.__is_field_filter(key) or Pagination.__is_valid_field(key)
            for key in cursor
        ]

        return all(valid_keys)

    @staticmethod
    def translate_filters(cursor: Cursor) -> Filters | None:
        """This method translates the given cursor returning a dictionary
        with the translated filters anf the original value.

        Example:
            ```Python
            >>> Pagination.translate_filters({"id":0,"select_related__campaign":10})
            {"filter": "select_related", "key":"campaign", "value":10}
            ```

        Args:
            cursor (Cursor): A decoded cursor.

        Returns:
            dict[str, typing.Any]: A dictionary with the filter key and the original value.
        """

        if not Pagination.check_valid_cursor(cursor):
            raise ValueError("Cannot translate an invalid cursor.")

        filters: Filters = {"filter": "", "key": "", "value": ""}

        for field in cursor:
            field_namespace = field.split("__", 1)

            if len(field_namespace) == 1:
                continue

            field_prefix = field_namespace[0]
            field_suffix = field_namespace[1]
            field_value = cursor.get(field)

            filters.update(
                {"filter": field_prefix, "key": field_suffix, "value": field_value}
            )

        if filters["filter"] == "":
            return None

        return filters

    @staticmethod
    def encode_cursor(cursor: Cursor) -> str:
        """Returns an encoded stringified cursor in base 64.

        Args:
            cursor (Cursor): A dictionary with the pagination metadata

        Returns:
            str: Returns a stringified dictionary in base 64.

        Raises:
            ValueError: When the cursor argument were not a valid cursor dictionary.
        """
        if not Pagination.check_valid_cursor(cursor):
            raise ValueError("The parameter 'cursor' is not a valid cursor dictionary.")

        serialized_json = json.dumps(cursor).encode("utf-8")
        encoded_cursor = b64encode(serialized_json).decode("utf-8")

        return encoded_cursor

    @staticmethod
    def decode_cursor(cursor: str) -> Cursor:
        """Returs a decoded cursor in a dictionary.

        Args:
            cursor (str): A stringified cursor in base 64.

        Returns:
            Cursor: A decoded cursor built with the deserilized string.

        Raises:
            ValueError: When the cursor argument were not a valid cursor dictionary.
        """
        decoded_cursor = b64decode(cursor.encode("utf-8")).decode("utf-8")
        deserialized_json = json.loads(decoded_cursor)

        if not Pagination.check_valid_cursor(deserialized_json):
            raise ValueError("The parameter 'cursor' is not a valid cursor dictionary.")

        return deserialized_json


def resolve_cursor(
    *, search_limit: int, encoded_cursor: str, model: typing.Type[ModelType]
) -> tuple[list[ModelType], str]:
    """This function is responsable of resolve the encoded cursor and return a list of
    specific entries.

    Args:
        search_limit (int): An integer number that limits the entries to serve.
        encoded_cursor (str): A cursor that is incoded in base 64.
        model (typing.Type[_ModelType]): A model to be queried.

    Returns:
        tuple[list[_ModelType], str]: A tuple with the queried entries and the next cursor.
    """

    # Tries by default, using the initial record.
    if encoded_cursor == "":
        encoded_cursor = Pagination.encode_cursor({"id": 1})

    cursor = Pagination.decode_cursor(encoded_cursor)

    cursor_indexation = cursor.get("id")
    cursor_filters = Pagination.translate_filters(cursor)

    retrieved_entries: list[ModelType] = []

    if cursor_filters == None:
        retrieved_entries = [
            entry for entry in model.objects.filter(id__gte=cursor_indexation)
        ]

    else:
        match cursor_filters["filter"]:
            case "select_related":
                retrieved_entries = [
                    entry
                    for entry in model.objects.filter(
                        id__gte=cursor_indexation
                    ).select_related(cursor_filters["key"])
                ]

    paginated_entries = retrieved_entries[: search_limit + 1]

    next_cursor_target = paginated_entries.pop(-1)
    next_cursor_target_with_id = next_cursor_target.id  # type: ignore

    next_cursor = Pagination.encode_cursor(
        {
            "id": next_cursor_target_with_id,
        }
    )

    return paginated_entries, next_cursor
