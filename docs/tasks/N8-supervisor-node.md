# Task N8: supervisor_node

This file contains the refined details for task N8.

---

### Context
- Decision = 'answer' if faithful and low uncertainty else 'dlq' (stub).

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Append audit with decision; keep logic deterministic.

### Unit Tests
- test_supervisor_answers_when_confident
- test_supervisor_dlq_when_unfaithful

### Evaluation
- pytest -q -k supervisor

### Regression
- State includes 'decision'.

### Audit Artifacts
- Ensure audit_trail includes: node="supervisor", decision

---
