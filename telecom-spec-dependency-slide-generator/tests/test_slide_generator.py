from src.models import Dependency, Document, GraphSummary
from src.slide_generator import SlideGenerator



def test_generate_creates_expected_slide_titles() -> None:
    generator = SlideGenerator()
    documents = [
        Document(id="a", title="Spec A", domain="core"),
        Document(id="b", title="Spec B", domain="data"),
    ]
    dependencies = [
        Dependency(
            source="a",
            target="b",
            type="prerequisite",
            criticality="high",
            confidence=0.9,
            basis="explicit",
            rationale="Detected dependency.",
            evidence=["depends on"],
        )
    ]
    summary = GraphSummary(
        total_documents=2,
        total_dependencies=1,
        critical_dependencies=1,
        circular_dependencies=0,
        interdomain_dependencies=1,
    )

    slides = generator.generate(documents, dependencies, summary)
    titles = [slide.title for slide in slides]

    assert titles == [
        "Executive Summary",
        "Domain Landscape",
        "High-Criticality Dependencies",
        "Recommendations",
    ]
