from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple

from .models import Dependency, Document, GraphSummary


class DependencyAnalyzer:
    """Analyze telecom specification documents and derive dependency relationships."""

    KEYWORD_RULES = {
        "prerequisite": ["requires", "depends on", "prerequisite", "subject to"],
        "interface": ["interface", "api", "reference point", "endpoint"],
        "integration": ["integrates with", "interworks with", "service exposure"],
        "data": ["subscriber data", "profile", "repository", "catalog", "data store"],
        "process": ["workflow", "provisioning", "activation", "sequence"],
        "event": ["notification", "trigger", "event", "alarm"],
        "conformance": ["shall comply", "conform", "alignment with"],
        "reference": ["refer to", "specified in", "as defined in"],
    }

    def analyze(self, documents: Iterable[Document]) -> List[Dependency]:
        docs = list(documents)
        dependencies: List[Dependency] = []

        for source in docs:
            source_text = (source.raw_text or "").lower()
            for target in docs:
                if source.id == target.id:
                    continue
                dependency = self._infer_dependency(source, target, source_text)
                if dependency is not None:
                    dependencies.append(dependency)

        return dependencies

    def build_summary(self, documents: Iterable[Document], dependencies: Iterable[Dependency]) -> GraphSummary:
        docs = list(documents)
        deps = list(dependencies)
        circular = self._count_cycles(deps)
        critical = sum(1 for dep in deps if dep.criticality == "high")

        domain_by_id = {doc.id: doc.domain for doc in docs}
        interdomain = sum(
            1
            for dep in deps
            if domain_by_id.get(dep.source) and domain_by_id.get(dep.target)
            and domain_by_id[dep.source] != domain_by_id[dep.target]
        )

        return GraphSummary(
            total_documents=len(docs),
            total_dependencies=len(deps),
            critical_dependencies=critical,
            circular_dependencies=circular,
            interdomain_dependencies=interdomain,
        )

    def _infer_dependency(self, source: Document, target: Document, source_text: str) -> Dependency | None:
        title_terms = {term.lower() for term in target.title.replace("/", " ").split() if len(term) > 3}
        matching_rules: List[Tuple[str, str]] = []

        target_mentioned = target.title.lower() in source_text or any(term in source_text for term in title_terms)

        for dep_type, keywords in self.KEYWORD_RULES.items():
            for keyword in keywords:
                if keyword in source_text and target_mentioned:
                    matching_rules.append((dep_type, keyword))

        if not matching_rules:
            return None

        dep_type = matching_rules[0][0]
        basis = "explicit" if target.title.lower() in source_text else "inferred"
        criticality = self._infer_criticality(dep_type)
        confidence = self._infer_confidence(dep_type, basis, len(matching_rules))

        evidence = [keyword for _, keyword in matching_rules[:3]]
        rationale = (
            f"Detected {dep_type} relationship from '{source.title}' to '{target.title}' "
            f"based on keywords: {', '.join(evidence)}."
        )

        return Dependency(
            source=source.id,
            target=target.id,
            type=dep_type,
            criticality=criticality,
            confidence=confidence,
            basis=basis,
            rationale=rationale,
            evidence=evidence,
        )

    @staticmethod
    def _infer_criticality(dep_type: str) -> str:
        if dep_type in {"prerequisite", "integration", "data"}:
            return "high"
        if dep_type in {"interface", "process", "conformance"}:
            return "medium"
        return "low"

    @staticmethod
    def _infer_confidence(dep_type: str, basis: str, match_count: int) -> float:
        base = 0.7 if basis == "explicit" else 0.55
        if dep_type in {"prerequisite", "reference"}:
            base += 0.1
        base += min(match_count, 3) * 0.05
        return min(base, 0.98)

    @staticmethod
    def _count_cycles(dependencies: Iterable[Dependency]) -> int:
        graph: Dict[str, Set[str]] = defaultdict(set)
        for dep in dependencies:
            graph[dep.source].add(dep.target)

        visited: Set[str] = set()
        stack: Set[str] = set()
        cycle_edges: Set[Tuple[str, str]] = set()

        def dfs(node: str) -> None:
            visited.add(node)
            stack.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in stack:
                    cycle_edges.add((node, neighbor))
            stack.remove(node)

        for node in list(graph):
            if node not in visited:
                dfs(node)

        return len(cycle_edges)
