# Task N3: ranker_node

This file contains the refined details for task N3.

---

### Context
- Pass-through with future dedup/diversity.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Return evidence as-is; append audit with kept count.

### Unit Tests
- test_ranker_passthrough

### Evaluation
- pytest -q -k ranker

### Regression
- Maintain input ordering.

### Audit Artifacts
- Ensure audit_trail includes: node="ranker", kept

---
