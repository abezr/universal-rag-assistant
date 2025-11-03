# Task UI1: Streamlit UI import and basic call

This file contains the refined details for task UI1.

---

### Context
- Headless import works; manual run displays sections.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Use build_graph and display answer/citations/uncertainty/validation.

### Unit Tests
- test_streamlit_import_succeeds

### Evaluation
- pytest -q -k streamlit_import (import-only)

### Regression
- No import-time side effects.

### Audit Artifacts
- Ensure audit_trail includes: N/A for UI

---
