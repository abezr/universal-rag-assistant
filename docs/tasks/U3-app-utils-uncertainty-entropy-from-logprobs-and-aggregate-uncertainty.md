# Task U3: app/utils/uncertainty.entropy_from_logprobs and aggregate_uncertainty

This file contains the refined details for task U3.

---

### Context
- Entropy computation and aggregation of span uncertainties.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Compute entropy from logprobs; aggregate spans to overall average; safe on empty.

### Unit Tests
- test_entropy_monotonicity: flatter distributions => higher entropy.
- test_aggregate_empty: returns overall 0.0.
- test_aggregate_average: correct averaging across spans.

### Evaluation
- pytest -q -k uncertainty

### Regression
- No negative entropy; no division-by-zero.

### Audit Artifacts
- Ensure audit_trail includes: N/A for utility

---
