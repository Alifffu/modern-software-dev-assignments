from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    - Please update the docs
    - Need to deploy by Friday
    - We should check the configuration
    Not actionable
    """.strip()
    items = extract_action_items(text)

    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items
    assert "Please update the docs" in items
    assert "Need to deploy by Friday" in items
    assert "We should check the configuration" in items
    assert "This is a note" not in items
    assert "Not actionable" not in items


