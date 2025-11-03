# Task N4: answerer_node

This file contains the refined details for task N4.

---

### Context
- Quote-first grounded answer and citations; abstain if no evidence.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Produce 'Q:' and 'A (grounded):' lines; include top-2 evidence lines and citations.

### Unit Tests
- test_answerer_with_evidence
- test_answerer_no_evidence

### Evaluation
- pytest -q -k answerer

### Regression
- No fabricated content; citation count matches evidence used.

### Audit Artifacts
- Ensure audit_trail includes: node="answerer", len

---
