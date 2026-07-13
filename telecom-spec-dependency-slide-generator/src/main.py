from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, List, Mapping, Any

from .dependency_analyzer import DependencyAnalyzer
from .models import AnalysisOutput, Document, Slide
from .parser import DocumentParser
from .slide_generator import SlideGenerator


def build_analysis(documents: Iterable[Document]) -> AnalysisOutput:
    """Run the full dependency-analysis pipeline for telecom specification documents."""
    docs = list(documents)
    analyzer = DependencyAnalyzer()
    dependencies = analyzer.analyze(docs)
    summary = analyzer.build_summary(docs, dependencies)
    slides = SlideGenerator().generate(docs, dependencies, summary)

    return AnalysisOutput(
        documents=docs,
        dependencies=dependencies,
        graph_summary=summary,
        slides=slides,
        recommendations=_collect_recommendations(slides),
    )


def parse_input_documents(payload: List[Mapping[str, Any]]) -> List[Document]:
    """Parse a list of raw document payloads into normalized Document objects."""
    parser = DocumentParser()
    return parser.parse_many(payload)


def save_analysis(output: AnalysisOutput, destination: str | Path) -> None:
    """Serialize analysis output as formatted JSON."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(output), indent=2), encoding="utf-8")


def _collect_recommendations(slides: Iterable[Slide]) -> List[str]:
    for slide in slides:
        if slide.title.lower() == "recommendations":
            return list(slide.content)
    return []


def run_example(destination: str | Path = Path("examples") / "generated_analysis_output.json") -> AnalysisOutput:
    """Run a small built-in example and persist the generated output."""
    example_payload = [
        {
            "id": "ts-001",
            "title": "5G Core Service Exposure Specification",
            "domain": "core-network",
            "version": "1.0",
            "organization": "3GPP",
            "summary": "Defines service exposure functions and related interfaces for 5G core capabilities.",
            "text": (
                "1 Overview\n"
                "This specification defines service exposure capabilities. "
                "It depends on subscriber data repositories and related profile access workflows.\n"
                "2 Integration\n"
                "The service exposure function integrates with subscriber data management."
            ),
        },
        {
            "id": "ts-002",
            "title": "Subscriber Data Interface Guidelines",
            "domain": "data-management",
            "version": "1.4",
            "organization": "ETSI",
            "summary": "Specifies data exchange expectations for subscriber profile access.",
            "text": (
                "1 Scope\n"
                "This document defines interface and profile access expectations for subscriber data."
            ),
        },
    ]

    documents = parse_input_documents(example_payload)
    result = build_analysis(documents)
    save_analysis(result, destination)
    return result


if __name__ == "__main__":
    output_path = Path("examples") / "generated_analysis_output.json"
    run_example(output_path)
    print(f"Analysis written to {output_path}")
