# CLI usage

Run the built-in example:

```bash
python -m src.cli --example
```

Run against a JSON input file:

```bash
python -m src.cli --input examples/input_documents.json --output examples/generated_analysis_output.json
```

Expected input format:

```json
[
  {
    "id": "ts-001",
    "title": "5G Core Service Exposure Specification",
    "domain": "core-network",
    "version": "1.0",
    "organization": "3GPP",
    "summary": "Defines service exposure functions and related interfaces for 5G core capabilities.",
    "text": "Full specification text here"
  }
]
```
