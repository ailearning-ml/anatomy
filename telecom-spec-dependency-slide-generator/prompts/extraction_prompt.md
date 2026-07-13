# Extraction Prompt

For each document, extract the following:

- document id
- title
- version
- primary domain
- purpose/summary
- referenced systems
- business entities
- inputs
- outputs
- references to other documents
- relevant sections
- phrases that indicate preconditions, blocking relationships, data consumption, or data production

## Expected output format

```json
{
  "id": "FS-001",
  "title": "Provisioning of Enterprise LTE Service",
  "version": "1.2",
  "domain": "Provisioning",
  "summary": "Short summary of the document purpose.",
  "systems": ["CRM", "Order Management", "Provisioning"],
  "entities": ["Customer", "Service Order", "MSISDN"],
  "inputs": ["Customer profile", "Validated order"],
  "outputs": ["Activation request", "Provisioned service"],
  "references": ["FS-003", "INT-002"],
  "sections": [
    {
      "title": "Preconditions",
      "text": "Customer profile must be validated according to FS-003."
    }
  ]
}
```
