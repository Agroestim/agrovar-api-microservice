from django.test import TestCase

from api.pagination import Cursor, Pagination


class TestPaginationSystem(TestCase):

    def test_encode_cursor_with_invalid_cursor_expecting_exception(self) -> None:
        with self.assertRaises(
            ValueError,
            msg="The 'encode_cursor' method must fail because it is reciving an invalid cursor argument.",
        ):
            Pagination.encode_cursor(
                {
                    "id": 1,
                    "invalid_field": 2,
                    "invalid_field__too": "abc",
                }
            )

    def test_decode_cursor_with_invalid_cursor_expecting_no_exception(self) -> None:
        with self.assertRaises(
            ValueError,
            msg="The 'decode_cursor' method must fail because is reciving an invalid cursor argument.",
        ):
            Pagination.decode_cursor("eyJpZCI6MSwgImludmFsaWRfZmllbGQiOjF9")

    def test_encode_cursor_with_valid_cursor_expecting_no_exception(self) -> None:
        valid_cursor: Cursor = {"id": 0}
        valid_encoded_cursor = "eyJpZCI6IDB9"

        try:
            encoded_cursor = Pagination.encode_cursor(valid_cursor)
        except:
            self.fail(
                "The 'encode_cursor' must run the test without raise any exception."
            )

        self.assertEqual(encoded_cursor, valid_encoded_cursor)

    def test_decode_cursor_with_valid_cursor_expecting_no_exception(self) -> None:
        valid_cursor: Cursor = {"id": 0, "select_related__crop_variety": 0}
        valid_encoded_cursor = (
            "eyJpZCI6IDAsICJzZWxlY3RfcmVsYXRlZF9fbG9jYXRpb24iOiAwfQ=="
        )

        try:
            decoded_cursor = Pagination.decode_cursor(valid_encoded_cursor)
        except:
            self.fail(
                "The 'decode_cursor' must run the test without raise any exception."
            )

        self.assertEqual(decoded_cursor, valid_cursor)
