from src.parser import DocumentParser


def test_parse_many_normalizes_and_splits_sections() -> None:
    parser = DocumentParser()
    documents = parser.parse_many(
        [
            {
                "id": "doc-1",
                "title": "Example Spec",
                "domain": "core",
                "text": "1 Overview\r\nThis    is   a test.\r\n2 Scope\r\nNEXT SECTION",
            }
        ]
    )

    assert len(documents) == 1
    document = documents[0]
    assert document.raw_text == "1 Overview\nThis is a test.\n2 Scope\nNEXT SECTION"
    assert len(document.sections) >= 2
    assert document.sections[0].startswith("1 Overview")
