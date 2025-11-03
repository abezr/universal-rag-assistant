# Task C1: app/config.Settings and AnswerPayload

This file contains the refined details for task C1.

---

### Context
- Settings management and API response schema.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Use pydantic-settings to read .env; AnswerPayload includes answer, citations, uncertainty, validation, decision.

### Unit Tests
- test_settings_env_override: env vars override defaults.
- test_answer_payload_schema: serialization/deserialization round-trip.

### Evaluation
- pytest -q -k settings

### Regression
- Do not rename keys; preserve defaults.

### Audit Artifacts
- Ensure audit_trail includes: N/A for config

---
