from seo_system.config import normalise_slug


def test_normalise_slug_basic():
    assert normalise_slug("US Expat Tax") == "us-expat-tax"


def test_normalise_slug_special_chars():
    assert normalise_slug("UK/US Tax Treaty (Dividends)") == "uk-us-tax-treaty-dividends"


def test_normalise_slug_already_slug():
    assert normalise_slug("us-expat-tax") == "us-expat-tax"


def test_normalise_slug_leading_trailing():
    assert normalise_slug("  hello world  ") == "hello-world"


def test_normalise_slug_numbers():
    assert normalise_slug("Top 10 Tips") == "top-10-tips"
