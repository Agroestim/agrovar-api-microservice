import json
import typing
from base64 import b64decode, b64encode

from django.db import models

type ModelType = type[models.Model]


MAX_SEARCH_LIMIT = 1000
"""Represents the max search limit for all query."""


class Filter(typing.TypedDict):
    """Represents a filtration method for the pagination system."""

    type: str
    """Represents the filtrarion method."""

    filter: dict[str, str]
    """Represents a lookup search."""


class Cursor(typing.TypedDict):
    """Represents a cursor for the pagination system."""

    id: int
    """Represents the next entry that cursor will target."""

    filter: Filter | None
    """Represents a query filtration parameter."""


class Pagination:

    CURSOR_FIELDS = ["id"]

    CURSOR_FILTERS = ["select_related"]
    CURSOR_LOOKUPS = ["location_origin__id", "crop_variety__id"]

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
        if not key.__contains__("__"):
            return False

        field_namespace = key.split("__", 2)

        if field_namespace[1] == "":
            return False

        field_prefix = field_namespace[0]
        field_suffix = field_namespace[1]

        return (
            field_prefix in Pagination.CURSOR_FILTERS
            and field_suffix in Pagination.CURSOR_LOOKUPS
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
    def __is_valid_filter(lookup: str) -> bool:
        """Check if the given lookup is valid.

        Args:
            lookup (str): A stringified dictionary with a django lookup expression.

        Returns:
            bool: True if its a valid lookup, False otherwise.
        """

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
            True
            or Pagination.__is_field_filter(key)
            or Pagination.__is_valid_field(key)
            for key in cursor
        ]

        return all(valid_keys)

    @staticmethod
    def translate_filters(cursor: Cursor) -> Filter | None:
        """This method translates the given cursor returning a dictionary
        with the translated filters anf the original value.

        Example:
            >>> Pagination.translate_filters({"id":0,"select_related__<lookup>":<value>})
            {"type": "select_related", "filter": {"<lookup>": <value>}}

        Args:
            cursor (Cursor): A decoded cursor.

        Returns:
            dict[str, typing.Any]: A dictionary with the filter key and the original value.
        """

        if not Pagination.check_valid_cursor(cursor):
            raise ValueError("Cannot translate an invalid cursor.")

        # Define an empty cursor by default.
        filters: Filter = {"type": "", "filter": {"": ""}}

        for __field in cursor:
            filter_namespace = __field.split("__", 1)

            # Continue when the namespace does not container a prefix.
            if len(filter_namespace) == 1:
                continue

            filter_type = filter_namespace[0]
            filter_lookup = filter_namespace[1]
            filter_lookup_value = cursor.get(__field)

            filters.update(
                {"type": filter_type, "filter": {filter_lookup: filter_lookup_value}}
            )

        # Return none if there is no any filters.
        if filters["type"] == "":
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

    # Check if the search limit exceeds the maximun search limit and raise an error if it happens.
    if search_limit > MAX_SEARCH_LIMIT:
        raise ValueError(
            f"Cannot query more than {MAX_SEARCH_LIMIT} entries at a time."
        )

    # Use a default cursor if the client does not provides ones.
    if encoded_cursor == "":
        encoded_cursor = "eyJpZCI6MX0="  # That represents this -> {"id":1}

    cursor = Pagination.decode_cursor(encoded_cursor)

    cursor_indexation = cursor.get("id")
    cursor_filters = Pagination.translate_filters(cursor)

    retrieved_entries: list[ModelType] = []

    # Perform the query using default search parameters.
    if cursor_filters == None:
        retrieved_entries = [
            entry for entry in model.objects.filter(id__gte=cursor_indexation)
        ]

    # Perform the query using search filters parameters.
    else:
        match cursor_filters["type"]:
            case "select_related":
                retrieved_entries = [
                    entry
                    for entry in model.objects.filter(id__gte=cursor_indexation).filter(
                        **cursor_filters["filter"]
                    )
                ]

    # Send and empty list when no items were retrieved.
    if len(retrieved_entries) == 0:
        return [], None

    # Send all items without a trailing cursor when there less items than the limit.
    if len(retrieved_entries) < search_limit:
        return retrieved_entries, None

    # When the retrieved items count exceeds the limit, send a portion of this and a cursor.
    else:
        paginated_entries = retrieved_entries[: search_limit + 1]

        next_cursor_target = paginated_entries.pop(-1)
        next_cursor_target_with_id = next_cursor_target.id  # type: ignore

        next_cursor = Pagination.encode_cursor({"id": next_cursor_target_with_id})

        return paginated_entries, next_cursor
