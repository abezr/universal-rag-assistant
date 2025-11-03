# Task U2: app/utils/citations.format_citations

This file contains the refined details for task U2.

---

### Context
- Render evidence list into [idx] source :: heading strings.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Handle missing fields gracefully; maintain stable 1-based ordering.

### Unit Tests
- test_citations_basic: with heading and source_uri.
- test_citations_missing_fields: handle missing heading/source.

### Evaluation
- pytest -q -k citations

### Regression
- Deterministic ordering; format remains stable.

### Audit Artifacts
- Ensure audit_trail includes: N/A for utility

---
