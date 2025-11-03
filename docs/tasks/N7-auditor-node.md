# Task N7: auditor_node

This file contains the refined details for task N7.

---

### Context
- Flag when high uncertainty or unfaithful.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Compute flag = (uncertainty.overall > 0.8) or (not faithful); append audit.

### Unit Tests
- test_auditor_flags_on_unfaithful
- test_auditor_not_flag_when_low_uncertainty_and_faithful

### Evaluation
- pytest -q -k auditor

### Regression
- Audit contains flag state.

### Audit Artifacts
- Ensure audit_trail includes: node="auditor", flag

---
