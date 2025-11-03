# Task U1: app/utils/logging.setup_logging

This file contains the refined details for task U1.

---

### Context
- Initialize root logger once with stdout handler and deterministic format.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Create a function that sets up logging only once. Prevent duplicate handlers across multiple imports/requests.

### Unit Tests
- test_logging_idempotent: calling setup_logging twice does not add duplicate handlers.
- test_logging_format: emitted line matches '%(asctime)s | %(levelname)s | %(name)s | %(message)s' (regex).

### Evaluation
- pytest -q -k logging

### Regression
- No duplicate logs across API requests; format unchanged.

### Audit Artifacts
- Ensure audit_trail includes: N/A for utility

---
