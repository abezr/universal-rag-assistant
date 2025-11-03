# Task N2: retriever_node and simple_keyword_match

This file contains the refined details for task N2.

---

### Context
- Stub retrieval over in-memory corpus; audit hits count.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Tokenize query; count term occurrences; sort desc by score; include metadata.

### Unit Tests
- test_retriever_hits
- test_retriever_scores_sorted
- test_retriever_empty_query

### Evaluation
- pytest -q -k retriever

### Regression
- Return items include score, source_uri, doc_id.

### Audit Artifacts
- Ensure audit_trail includes: node="retriever", hits

---
