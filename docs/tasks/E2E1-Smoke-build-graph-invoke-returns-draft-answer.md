# Task E2E1: Smoke: build_graph().invoke returns draft_answer

This file contains the refined details for task E2E1.

---

### Context
- End-to-end minimal graph invocation.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Keep tests/test_smoke.py green with current scaffold.

### Unit Tests
- test_graph_smoke

### Evaluation
- pytest -q -k smoke

### Regression
- Always pass regardless of LangGraph presence.

### Audit Artifacts
- Ensure audit_trail includes: full node sequence during invocation
