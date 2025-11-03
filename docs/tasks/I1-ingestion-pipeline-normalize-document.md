# Task I1: ingestion.pipeline.normalize_document

This file contains the refined details for task I1.

---

### Context
- Decode bytes to text; produce document/sections structure.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Handle decoding errors with ignore; attach minimal metadata.

### Unit Tests
- test_normalize_document_basic

### Evaluation
- pytest -q -k normalize_document

### Regression
- Stable keys: document, sections, text.

### Audit Artifacts
- Ensure audit_trail includes: N/A for ingestion stub

---
