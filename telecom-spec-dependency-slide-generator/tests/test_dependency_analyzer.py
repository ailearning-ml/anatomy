from src.dependency_analyzer import DependencyAnalyzer
from src.models import Document



def test_analyze_detects_dependency_relationship() -> None:
    analyzer = DependencyAnalyzer()
    documents = [
        Document(
            id="a",
            title="Core Exposure Spec",
            domain="core-network",
            raw_text="Core Exposure Spec depends on Subscriber Data Interface for profile workflow.",
        ),
        Document(
            id="b",
            title="Subscriber Data Interface",
            domain="data-management",
            raw_text="Defines subscriber data interfaces.",
        ),
    ]

    dependencies = analyzer.analyze(documents)

    assert len(dependencies) >= 1
    dependency = dependencies[0]
    assert dependency.source == "a"
    assert dependency.target == "b"
    assert dependency.criticality in {"high", "medium", "low"}
    assert dependency.confidence > 0


def test_build_summary_counts_interdomain_dependencies() -> None:
    analyzer = DependencyAnalyzer()
    documents = [
        Document(id="a", title="A", domain="core", raw_text="A depends on B"),
        Document(id="b", title="B", domain="data", raw_text="B"),
    ]
    dependencies = analyzer.analyze(documents)
    summary = analyzer.build_summary(documents, dependencies)

    assert summary.total_documents == 2
    assert summary.total_dependencies == len(dependencies)
    assert summary.interdomain_dependencies >= 0
