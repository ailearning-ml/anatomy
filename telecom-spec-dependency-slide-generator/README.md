# Telecom Spec Dependency Slide Generator

A Kiro-oriented skill package for analyzing telecommunications functional specification documents and generating structured dependency analysis outputs that can be used to build presentation materials.

## What it does

This skill helps architecture, business analysis, delivery, and governance teams understand:

- which specification documents depend on which others;
- which telecom domains and systems are most critical;
- which documents block downstream implementation work;
- where circular dependencies may exist;
- which implementation sequence is most sensible.

## Current implementation status

The current Python implementation provides:

- structured document parsing from JSON-like payloads;
- rule-based dependency inference across documents;
- graph summary generation;
- generation of presentation-oriented slide content objects;
- a CLI for running the built-in example or processing a JSON input file;
- a basic automated test suite.

## Package contents

- `skill.yaml` — skill metadata and behavior definition
- `prompts/` — extraction, dependency, and slide-generation prompts
- `schemas/` — JSON schemas for structured outputs
- `templates/` — taxonomy, rules, and slide templates
- `examples/` — sample config and example output
- `docs/` — architecture and execution flow
- `src/` — Python implementation
- `tests/` — basic automated tests

## Inputs

Currently supported inputs:

- a JSON file containing a top-level list of document objects;
- programmatic document payloads passed into the Python API;
- direct text file parsing when metadata is provided in code.

Each document object should contain:

- `id`
- `title`
- `domain`
- `text`

Optional fields include:

- `version`
- `organization`
- `summary`

## Outputs

Currently implemented outputs:

- a single JSON analysis file produced by `save_analysis(...)`;
- structured slide content objects in memory;
- summary statistics and inferred dependency relationships.

Planned or not yet implemented:

- `dependency_graph.json`
- `dependency_matrix.csv`
- `document_summary.json`
- `risks_and_gaps.json`
- `dependency_anatomy.pptx`

## Current slide structure

The current `SlideGenerator` produces these slides:

1. Executive Summary
2. Domain Landscape
3. High-Criticality Dependencies
4. Recommendations

## Local Python usage

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r telecom-spec-dependency-slide-generator/requirements.txt
```

Run the built-in example:

```bash
python -m src.cli --example
```

Run against a JSON input file:

```bash
python -m src.cli \
  --input telecom-spec-dependency-slide-generator/examples/input_documents.json \
  --output telecom-spec-dependency-slide-generator/examples/generated_analysis_output.json
```

## Testing

Run the test suite with:

```bash
pytest telecom-spec-dependency-slide-generator/tests
```

## Notes

- The current implementation is intentionally modular and extensible.
- Dependency detection is currently rule-based and can be expanded with richer parsing or model-assisted extraction.
- The project includes presentation-oriented slide content generation, but it does not yet generate a `.pptx` file directly.
