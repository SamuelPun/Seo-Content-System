from build_output import build_html


def test_build_html_escapes_title_and_description():
    html_out = build_html(
        title='Tax Filing & Deadlines: "What You Need"',
        description="Rates <5% apply & save",
        url="https://example.com/a",
        body_html="<p>body</p>",
        schemas=None,
    )
    assert "<title>Tax Filing &amp; Deadlines: &quot;What You Need&quot;</title>" in html_out
    assert 'content="Rates &lt;5% apply &amp; save"' in html_out


def test_build_html_escapes_script_close_in_schema():
    html_out = build_html(
        title="T",
        description="D",
        url="https://example.com/a",
        body_html="<p>body</p>",
        schemas=[{"description": "</script><script>alert(1)</script>"}],
    )
    assert "</script><script>alert(1)</script>" not in html_out
