# Task D1: dlq.queue.FileDLQ.enqueue and stream

This file contains the refined details for task D1.

---

### Context
- Append-only JSONL with safe directory creation.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- On init create directories; enqueue writes JSONL; stream yields parsed lines.

### Unit Tests
- test_dlq_enqueue_and_stream

### Evaluation
- pytest -q -k dlq

### Regression
- No invalid JSON; preserves insertion order.

### Audit Artifacts
- Ensure audit_trail includes: N/A for DLQ infra

---
