from unittest.mock import patch

from fetch_url import fetch_to_markdown


def test_fetch_to_markdown_applies_requested_timeout():
    with patch("fetch_url.trafilatura.fetch_url", return_value="<html></html>") as mock_fetch, \
         patch("fetch_url.trafilatura.extract", return_value="body text"):
        fetch_to_markdown("https://example.com", timeout=7)

    _, kwargs = mock_fetch.call_args
    assert kwargs["config"].get("DEFAULT", "DOWNLOAD_TIMEOUT") == "7"
