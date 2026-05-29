import io
import json
import unittest
from unittest.mock import MagicMock, patch

from func import handler


class TestHandler(unittest.TestCase):
    """Tests for the Oracle Function handler."""

    def setUp(self):
        self.ctx = MagicMock()

    def _make_body(self, payload):
        """Helper to create a BytesIO body from a dict or string."""
        if isinstance(payload, str):
            return io.BytesIO(payload.encode("utf-8"))
        return io.BytesIO(json.dumps(payload).encode("utf-8"))

    def _get_response_message(self, resp):
        """Extract the message string from a Response."""
        data = json.loads(resp.response_data)
        return data["message"]

    # --- Happy path ---

    def test_returns_custom_name(self):
        """Should greet with the provided name."""
        data = self._make_body({"name": "Alice"})
        resp = handler(self.ctx, data)
        self.assertEqual(self._get_response_message(resp), "Hello Alice")

    def test_returns_default_name_when_no_body(self):
        """Should greet with 'World' when the body is empty."""
        data = io.BytesIO(b"")
        resp = handler(self.ctx, data)
        self.assertEqual(self._get_response_message(resp), "Hello World")

    def test_returns_default_name_when_key_missing(self):
        """Should greet with 'World' when JSON is valid but 'name' key is absent."""
        data = self._make_body({"foo": "bar"})
        resp = handler(self.ctx, data)
        self.assertEqual(self._get_response_message(resp), "Hello World")

    # --- Edge cases ---

    def test_invalid_json_returns_default(self):
        """Should fall back to 'World' on malformed JSON."""
        data = self._make_body("not-json")
        resp = handler(self.ctx, data)
        self.assertEqual(self._get_response_message(resp), "Hello World")

    def test_empty_name_value(self):
        """Should return an empty name if explicitly set to empty string."""
        data = self._make_body({"name": ""})
        resp = handler(self.ctx, data)
        self.assertEqual(self._get_response_message(resp), "Hello ")

    def test_name_with_special_characters(self):
        """Should handle names with special characters."""
        data = self._make_body({"name": "O'Brien <script>"})
        resp = handler(self.ctx, data)
        self.assertEqual(self._get_response_message(resp), "Hello O'Brien <script>")

    def test_numeric_name(self):
        """Should handle a numeric name value."""
        data = self._make_body({"name": 42})
        resp = handler(self.ctx, data)
        self.assertEqual(self._get_response_message(resp), "Hello 42")

    # --- Response structure ---

    def test_response_content_type(self):
        """Response should set JSON content type header on the context."""
        data = self._make_body({"name": "Test"})
        handler(self.ctx, data)
        self.ctx.SetResponseHeaders.assert_called_once()
        headers = self.ctx.SetResponseHeaders.call_args[0][0]
        self.assertEqual(headers["Content-Type"], "application/json")

    def test_response_body_is_valid_json(self):
        """Response body should be parseable JSON with a 'message' key."""
        data = self._make_body({"name": "Test"})
        resp = handler(self.ctx, data)
        body = json.loads(resp.response_data)
        self.assertIn("message", body)

    # --- Logging ---

    def test_invalid_json_logs_warning(self):
        """Should log a warning when JSON parsing fails."""
        data = self._make_body("bad-json")
        with patch("func.logger") as mock_logger:
            handler(self.ctx, data)
            mock_logger.warning.assert_called_once()

    def test_valid_request_logs_info(self):
        """Should log an info message on every request."""
        data = self._make_body({"name": "Alice"})
        with patch("func.logger") as mock_logger:
            handler(self.ctx, data)
            mock_logger.info.assert_called_once()


if __name__ == "__main__":
    unittest.main()
