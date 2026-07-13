from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional


DependencyType = Literal[
    "prerequisite",
    "interface",
    "integration",
    "data",
    "process",
    "event",
    "conformance",
    "reference",
]

Criticality = Literal["low", "medium", "high"]
DependencyBasis = Literal["explicit", "inferred"]


@dataclass(slots=True)
class Document:
    """Normalized telecom specification document metadata and content."""

    id: str
    title: str
    domain: str
    version: Optional[str] = None
    organization: Optional[str] = None
    summary: Optional[str] = None
    sections: List[str] = field(default_factory=list)
    raw_text: Optional[str] = None


@dataclass(slots=True)
class Dependency:
    """A dependency relationship between two telecom artifacts."""

    source: str
    target: str
    type: DependencyType
    criticality: Criticality
    confidence: float
    basis: DependencyBasis
    rationale: str
    evidence: List[str] = field(default_factory=list)


@dataclass(slots=True)
class GraphSummary:
    """High-level aggregate statistics over dependency relationships."""

    total_documents: int
    total_dependencies: int
    critical_dependencies: int
    circular_dependencies: int
    interdomain_dependencies: int


@dataclass(slots=True)
class Slide:
    """Presentation-ready slide structure."""

    title: str
    purpose: str
    content: List[str] = field(default_factory=list)


@dataclass(slots=True)
class AnalysisOutput:
    """Top-level structured output for dependency analysis."""

    documents: List[Document] = field(default_factory=list)
    dependencies: List[Dependency] = field(default_factory=list)
    graph_summary: Optional[GraphSummary] = None
    slides: List[Slide] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
