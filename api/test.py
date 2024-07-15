from django.test import TestCase

from api.pagination import Cursor, Pagination


class TestPaginationSystem(TestCase):

    def test_encode_cursor_with_invalid_cursor(self) -> None:
        pagination = Pagination()

        invalid_cursor = {
            "id": 0,
            "select_by_related_field": "",
            "invalid_field": "",
        }

        with self.assertRaises(
            ValueError,
            msg="The 'encode_cursor' method must fail because it is reciving an invalid cursor argument.",
        ):
            pagination.encode_cursor(invalid_cursor)  # type: ignore

    def test_decode_cursor_with_invalid_cursor(self) -> None:
        pagination = Pagination()

        invalid_encoded_cursor = "eyJpZCI6IDAsInNlbGVjdF9ieV9yZWxhdGVkX2ZpZWxkIjogIiIsImludmFsaWRfZmllbGQiOiAiIn0="

        with self.assertRaises(
            ValueError,
            msg="The 'decode_cursor' method must fail because it isreciving an invalid cursor argument.",
        ):
            pagination.decode_cursor(invalid_encoded_cursor)

    def test_encode_cursor_with_valid_cursor(self) -> None:
        pagination = Pagination()

        valid_cursor: Cursor = {"id": 0, "select_by_related_field": ""}
        valid_encoded_cursor = (
            "eyJpZCI6IDAsICJzZWxlY3RfYnlfcmVsYXRlZF9maWVsZCI6ICIifQ=="
        )

        try:
            encoded_cursor = pagination.encode_cursor(valid_cursor)
        except:
            self.fail(
                "The 'encode_cursor' must run the test without raise any exception."
            )

        self.assertEqual(encoded_cursor, valid_encoded_cursor)

    def test_decode_cursor_with_valid_cursor(self) -> None:
        pagination = Pagination()

        valid_cursor: Cursor = {"id": 0, "select_by_related_field": ""}
        valid_encoded_cursor = (
            "eyJpZCI6IDAsICJzZWxlY3RfYnlfcmVsYXRlZF9maWVsZCI6ICIifQ=="
        )

        try:
            decoded_cursor = pagination.decode_cursor(valid_encoded_cursor)
        except:
            self.fail(
                "The 'decode_cursor' must run the test without raise any exception."
            )

        self.assertEqual(decoded_cursor, valid_cursor)
