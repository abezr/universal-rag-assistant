# Task N5: uncertainty_node

This file contains the refined details for task N5.

---

### Context
- Aggregate stub spans: low when evidence exists; high otherwise.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Set example span entropies and aggregate; append audit with overall.

### Unit Tests
- test_uncertainty_with_evidence_low
- test_uncertainty_without_evidence_high

### Evaluation
- pytest -q -k uncertainty_node

### Regression
- Uncertainty contains 'overall' and 'spans'.

### Audit Artifacts
- Ensure audit_trail includes: node="uncertainty", overall

---
