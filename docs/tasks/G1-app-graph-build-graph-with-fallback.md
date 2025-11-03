# Task G1: app/graph/build_graph with fallback

This file contains the refined details for task G1.

---

### Context
- Graph builds using LangGraph if present; otherwise uses sequential pipeline.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Try import; on failure, provide SimplePipeline.invoke calling nodes in order.

### Unit Tests
- test_graph_builds_without_langgraph: simulate import error and verify pipeline.
- test_graph_invocation_flow: audit_trail contains all nodes in order.

### Evaluation
- pytest -q -k graph

### Regression
- Resilient build path; do not break if LangGraph missing.

### Audit Artifacts
- Ensure audit_trail includes: ordered entries per node

---
