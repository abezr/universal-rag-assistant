# Task N6: validator_node

This file contains the refined details for task N6.

---

### Context
- Faithfulness = True if evidence found; else False.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Inspect retrieved_evidence and emit validation_reports; append audit.

### Unit Tests
- test_validator_faithful_with_evidence
- test_validator_unfaithful_without_evidence

### Evaluation
- pytest -q -k validator

### Regression
- validation_reports schema stable.

### Audit Artifacts
- Ensure audit_trail includes: node="validator", faithful

---
