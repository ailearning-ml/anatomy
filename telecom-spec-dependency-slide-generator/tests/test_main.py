import json
from pathlib import Path

from src.main import build_analysis, parse_input_documents, save_analysis


SAMPLE_PAYLOAD = [
    {
        "id": "ts-001",
        "title": "Core Exposure Spec",
        "domain": "core-network",
        "version": "1.0",
        "organization": "3GPP",
        "summary": "Defines service exposure.",
        "text": "This specification depends on Subscriber Data Interface and includes workflow sequencing.",
    },
    {
        "id": "ts-002",
        "title": "Subscriber Data Interface",
        "domain": "data-management",
        "version": "1.1",
        "organization": "ETSI",
        "summary": "Defines profile access.",
        "text": "This document defines interface expectations for subscriber data.",
    },
]


def test_build_analysis_generates_summary_and_slides(tmp_path: Path) -> None:
    documents = parse_input_documents(SAMPLE_PAYLOAD)
    output = build_analysis(documents)

    assert len(output.documents) == 2
    assert output.graph_summary is not None
    assert output.graph_summary.total_documents == 2
    assert len(output.slides) == 4
    assert output.recommendations

    destination = tmp_path / "analysis.json"
    save_analysis(output, destination)
    saved = json.loads(destination.read_text(encoding="utf-8"))
    assert saved["graph_summary"]["total_documents"] == 2
