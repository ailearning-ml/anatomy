from __future__ import annotations

from collections import Counter
from typing import Iterable, List

from .models import Dependency, Document, GraphSummary, Slide


class SlideGenerator:
    """Generate presentation-ready slides from telecom dependency analysis."""

    def generate(
        self,
        documents: Iterable[Document],
        dependencies: Iterable[Dependency],
        summary: GraphSummary,
    ) -> List[Slide]:
        docs = list(documents)
        deps = list(dependencies)

        return [
            self._build_executive_summary(docs, deps, summary),
            self._build_domain_landscape(docs, deps),
            self._build_high_criticality_slide(docs, deps),
            self._build_recommendations_slide(deps, summary),
        ]

    def _build_executive_summary(
        self,
        documents: List[Document],
        dependencies: List[Dependency],
        summary: GraphSummary,
    ) -> Slide:
        domains = sorted({doc.domain for doc in documents})
        content = [
            f"Analyzed {summary.total_documents} documents spanning {len(domains)} domains.",
            f"Identified {summary.total_dependencies} dependencies, including {summary.critical_dependencies} high-criticality relationships.",
            f"Detected {summary.interdomain_dependencies} cross-domain dependencies and {summary.circular_dependencies} circular dependency signals.",
        ]
        if domains:
            content.append(f"Domains covered: {', '.join(domains)}.")

        return Slide(
            title="Executive Summary",
            purpose="Provide a concise overview of the telecom dependency landscape.",
            content=content,
        )

    def _build_domain_landscape(
        self,
        documents: List[Document],
        dependencies: List[Dependency],
    ) -> Slide:
        counts = Counter(doc.domain for doc in documents)
        doc_by_id = {doc.id: doc for doc in documents}
        cross_domain = []

        for dep in dependencies:
            source = doc_by_id.get(dep.source)
            target = doc_by_id.get(dep.target)
            if not source or not target:
                continue
            if source.domain != target.domain:
                cross_domain.append(
                    f"{source.title} ({source.domain}) → {target.title} ({target.domain}) [{dep.type}]"
                )

        content = [f"{domain}: {count} document(s)" for domain, count in sorted(counts.items())]
        if cross_domain:
            content.append("Cross-domain links:")
            content.extend(cross_domain[:5])
        else:
            content.append("No cross-domain links were detected.")

        return Slide(
            title="Domain Landscape",
            purpose="Show document distribution and notable cross-domain relationships.",
            content=content,
        )

    def _build_high_criticality_slide(
        self,
        documents: List[Document],
        dependencies: List[Dependency],
    ) -> Slide:
        doc_by_id = {doc.id: doc for doc in documents}
        high_risk = [dep for dep in dependencies if dep.criticality == "high"]

        content: List[str] = []
        for dep in high_risk[:6]:
            source = doc_by_id.get(dep.source)
            target = doc_by_id.get(dep.target)
            source_name = source.title if source else dep.source
            target_name = target.title if target else dep.target
            content.append(
                f"{source_name} → {target_name} ({dep.type}, {dep.basis}, confidence {dep.confidence:.2f})"
            )

        if not content:
            content.append("No high-criticality dependencies were detected.")

        return Slide(
            title="High-Criticality Dependencies",
            purpose="Highlight the relationships most likely to affect interoperability and delivery risk.",
            content=content,
        )

    def _build_recommendations_slide(
        self,
        dependencies: List[Dependency],
        summary: GraphSummary,
    ) -> Slide:
        inferred_count = sum(1 for dep in dependencies if dep.basis == "inferred")
        content = [
            "Validate all high-criticality relationships with domain subject matter experts.",
            "Preserve evidence traces so each dependency can be mapped back to source text.",
        ]

        if inferred_count:
            content.append(
                f"Review {inferred_count} inferred dependencies to confirm whether they should be treated as architectural constraints."
            )
        if summary.circular_dependencies:
            content.append(
                f"Investigate {summary.circular_dependencies} possible circular dependency patterns before finalizing implementation sequencing."
            )
        if summary.interdomain_dependencies:
            content.append(
                "Coordinate change management across domains because the dependency graph shows cross-domain coupling."
            )

        return Slide(
            title="Recommendations",
            purpose="Summarize follow-up actions for architecture and delivery planning.",
            content=content,
        )
