# Task N1: router_node

This file contains the refined details for task N1.

---

### Context
- Intent classification and audit append.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Classify lookup/synthesis/policy by keywords; append audit entry with intent.

### Unit Tests
- test_router_synthesis_intent
- test_router_policy_intent
- test_router_default_lookup

### Evaluation
- pytest -q -k router

### Regression
- Default remains 'lookup'.

### Audit Artifacts
- Ensure audit_trail includes: node="router", intent

---
