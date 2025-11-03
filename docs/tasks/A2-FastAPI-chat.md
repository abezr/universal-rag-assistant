# Task A2: FastAPI /chat

This file contains the refined details for task A2.

---

### Context
- Accepts message; invokes graph; returns AnswerPayload.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Pydantic request model; call graph.invoke; adapt fields.

### Unit Tests
- test_chat_endpoint_basic
- test_chat_abstain_when_no_hits

### Evaluation
- pytest -q -k chat

### Regression
- Keys stable: answer, citations, uncertainty, validation, decision.

### Audit Artifacts
- Ensure audit_trail includes: end-to-end trace available via nodes

---
