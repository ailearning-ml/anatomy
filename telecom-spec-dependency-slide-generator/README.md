# Telecom Spec Dependency Slide Generator

A Kiro-oriented skill package for analyzing telecommunications functional specification documents and generating a PowerPoint-style slide deck that shows the anatomy of dependencies across documents, systems, interfaces, processes, and data.

## What it does

This skill helps architecture, business analysis, delivery, and governance teams understand:

- which specification documents depend on which others;
- which telecom domains and systems are most critical;
- which documents block downstream implementation work;
- where circular dependencies, gaps, and conflicts exist;
- which implementation sequence is most sensible.

## Package contents

- `skill.yaml` — skill metadata and behavior definition
- `prompts/` — extraction, dependency, and slide-generation prompts
- `schemas/` — JSON schemas for structured outputs
- `templates/` — taxonomy, rules, and slide templates
- `examples/` — sample config and example output
- `docs/` — architecture and execution flow
- `src/` — initial Python implementation

## Inputs

- A folder containing `.pdf`, `.docx`, `.md`, `.txt`, `.xlsx`, and/or `.csv` specification files
- Optional configuration such as project name, confidence threshold, output formats, and telecom taxonomy

## Outputs

- `dependency_graph.json`
- `dependency_matrix.csv`
- `document_summary.json`
- `risks_and_gaps.json`
- `dependency_anatomy.pptx`

## Presentation structure

1. Cover
2. Executive summary
3. Global dependency map
4. Domain clusters
5. Dependency matrix
6. Critical paths
7. Circular dependencies
8. Gaps and conflicts
9. One slide per document
10. Recommendations

## Local Python usage

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r telecom-spec-dependency-slide-generator/requirements.txt
python telecom-spec-dependency-slide-generator/src/main.py \
  --input-path ./specs \
  --output-path ./out \
  --project-name "Telecom Transformation Program" \
  --analysis-name "Dependency Anatomy"
```

## Notes

- The initial Python implementation is intentionally modular and extensible.
- PDF/DOCX parsing is lightweight in the starter version and can be upgraded.
- The slide deck generation uses `python-pptx` and produces a first-pass presentation structure.
