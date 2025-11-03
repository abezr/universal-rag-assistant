# Task X1: indexing.chunking.simple_chunk_sections

This file contains the refined details for task X1.

---

### Context
- Split sections into fixed-size chunks; propagate metadata.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Chunk by max_len; include doc_id, source_uri, heading, hash.

### Unit Tests
- test_chunking_splits_text
- test_chunking_metadata_present

### Evaluation
- pytest -q -k chunking

### Regression
- No empty chunks; consistent chunk counts.

### Audit Artifacts
- Ensure audit_trail includes: N/A for indexing stub

---
