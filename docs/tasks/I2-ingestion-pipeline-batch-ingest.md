# Task I2: ingestion.pipeline.batch_ingest

This file contains the refined details for task I2.

---

### Context
- Map normalize_document over inputs; maintain order.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Zip blobs and uris; return list of normalized docs.

### Unit Tests
- test_batch_ingest_lengths_match

### Evaluation
- pytest -q -k batch_ingest

### Regression
- Deterministic ordering.

### Audit Artifacts
- Ensure audit_trail includes: N/A for ingestion stub

---
