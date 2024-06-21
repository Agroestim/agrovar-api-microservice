import typing
from base64 import b64decode, b64encode

from django.db import models

ModelType = typing.TypeVar("ModelType", bound=models.Model)


def decode_campaign_document_id_cursor(cursor: str) -> int:
    """Decode the given base64 str and return a new cursor.

    Args:
        cursor (str): A encoded dictionary with the next cursor.

    Returns:
        int: The next campaign document id cursor.
    """

    cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
    cursor_data_id_value = cursor_data.split(":")[1]
    return int(cursor_data_id_value)


def encode_campaign_document_id_cursor(id: int) -> str:
    """Encode the given campaign document id and return a
    encode dictionary with the next cursor.

    Args:
        id (int): The campaign document id to be encoded.

    Returns:
        str: A new encoded object with a cursor object.
    """

    return b64encode(f"id:{id}".encode("ascii")).decode("ascii")


def use_resolve_cursor_hook(
    limit: int, cursor: typing.Optional[str], model: typing.Type[ModelType]
):
    entry_id: int = 0

    if cursor is not None and cursor != "":
        entry_id = decode_campaign_document_id_cursor(cursor)

    filtred_entries = [entry for entry in model.objects.filter(id__gte=entry_id)]

    sliced_entries = filtred_entries[: limit + 1]

    if not len(sliced_entries) > limit:
        next_cursor = None

    last_entry = filtred_entries.pop(-1)

    try:
        next_cursor = encode_campaign_document_id_cursor(last_entry.id)  # type: ignore

    except Exception:
        next_cursor = None

    return sliced_entries, next_cursor
