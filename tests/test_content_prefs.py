from seo_system.onboard.qa import build_qa_text


def test_build_qa_text_includes_content_prefs():
    data = {
        "name": "Acme",
        "website": "https://acme.com",
        "industry": "Tax advisory",
        "primary_market": "UK SMEs",
        "voice_style": "direct",
        "reader_feeling": "confident",
        "voice_phrases": ["clarity", "no jargon"],
        "voice_never": ["vague advice"],
        "differentiator": "real practitioners",
        "jargon_policy": "explain on first use",
        "extra_voice_notes": "",
        "opening_pattern": "Situation first",
        "opinion_style": "Opinionated",
        "teaching_style": "Worked examples",
        "editorial_asides": "Honestly, that's the bar.",
        "howto_format": "Numbered steps",
        "preferred_formats": "Guides and comparisons",
        "article_depth": "In-depth (2000+ words)",
        "structural_defaults": "No listicles; tables for data only",
        "audience_segments": [],
        "content_goals": "- Organic traffic",
    }
    result = build_qa_text(data)
    assert "Preferred content formats: Guides and comparisons" in result
    assert "Article depth: In-depth (2000+ words)" in result
    assert "Structural defaults: No listicles; tables for data only" in result
