# Dependency Prompt

Analyze the extracted documents and identify dependencies between them.

## You must:
- detect explicit and implicit dependencies;
- classify each dependency by type;
- assign a criticality level;
- record textual evidence;
- provide a confidence score;
- identify whether the relationship is intra-domain or cross-domain.

## Dependency types
- prerequisite
- functional
- interface
- integration
- data
- process
- event
- regulatory
- blocking
- upstream
- downstream

## Expected output format

```json
{
  "from": "FS-001",
  "to": "FS-003",
  "type": "prerequisite",
  "criticality": "high",
  "confidence": 0.91,
  "explicit": true,
  "interdomain": true,
  "evidence": "Customer profile must be validated according to FS-003.",
  "source_section": "Preconditions"
}
```
