# Universal Data Assistant — Backlog and Tasks

Cooperative AI system for precise, cited Q&A over fuzzy internal documentation, built with LangGraph (fallback to sequential pipeline), with uncertainty tracking, hallucination mitigation, citations, cross-validation, and DLQ-driven human-in-the-loop.

---

## Pre-flight baseline
- Run: `python scaffold.py`
- Create venv and install deps: `python -m venv .venv && .venv/Scripts/Activate.ps1`; `pip install -r requirements.txt`; `pip install pytest`
- Run tests: `pytest -q` (initially passing)
- Start API: `uvicorn app.main:app --reload` and verify `/health`

## Global audit and governance expectations
- Every graph node appends to audit_trail in state: `{node, info...}`
- Decisions and routing recorded: intent, evidence count, validation results, uncertainty score, final decision
- DLQ items contain full envelope (reason_code, artifacts) when applicable
- Prompts, model IDs, parameters, and citations are traceable in audit trail (stubbed initially; full fidelity later)

## Phased execution order
- Phase 0: Scaffold and baseline run
- Phase 1: Core utilities and config (U1–U3, C1)
- Phase 2: Graph/build/state (G1–G2)
- Phase 3: Node implementations (N1–N8)
- Phase 4: Ingestion and indexing (I1–I2, X1–X2)
- Phase 5: DLQ (D1)
- Phase 6: API and UI (A1–A2, UI1)
- Phase 7: E2E smoke and stabilization (E2E1)

## Evaluation and regression
- For each task, add unit tests and run: `pytest -q -k <scope>`
- API smoke: `uvicorn app.main:app --reload` then GET `/health`, POST `/chat`
- UI smoke: `streamlit run app/ui/app.py`
- Maintain regression: do not break audit trail schema or API response model

## Exit criteria
- All tests pass
- `/health` returns `{ "status": "ok" }`
- `/chat` returns AnswerPayload schema
- Streamlit UI renders and answers with citations, uncertainty, validation
- Audit trail includes entries from all nodes
- No duplicate log handlers; no regressions against suite

---

## Regression Suites Summary

### Core regression suites
- Logging: no duplicate handlers; stable format
- Citations: deterministic order, 1-based, resilient to missing metadata
- Uncertainty: non-negative entropy; aggregation stable on empty spans
- Settings and payload: env overrides; schema backward compatible
- Graph: builds with and without LangGraph; ordered audit trail
- Nodes: each appends audit; deterministic decisions for same state
- Ingestion/Indexing: stable chunk sizes/metadata; deterministic ordering
- DLQ: append-only JSONL; stream reproduces items in order
- API: response schema; content types and status codes stable
- UI: import-time success; no heavy side effects

### Contract stability tests
- tests/test_api_contract.py: verify /chat and /health contracts
- tests/test_audit_trail.py: presence and order of node audit entries
- tests/test_decision_policy.py: supervisor decisions by scenario

### Command checklist per change
- Run: `pytest -q`
- If API touched: manual `/health` and `/chat` checks
- If UI touched: import app.ui.app in a Python REPL and ensure no ImportError

---

## Orchestrator Prompt (for CI/automation)

```
System:
You are an AI implementation orchestrator. Execute tasks sequentially with atomic commits. Never skip tests. Maintain backward compatibility and ensure all tests are green at each step.

Constraints:
- OS: Windows
- Working directory: D:/study/ai/universal-rag-assistant
- First, run: python scaffold.py
- Create venv and install dependencies from requirements.txt. Install pytest if missing.
- Use `pytest -q` frequently. Favor small PR-sized steps.

Priorities:
1) Ensure baseline passes smoke tests.
2) Implement tasks U1��UI1 in the defined order.
3) For each task: write code, write tests, run tests, fix until green.
4) Preserve audit trail fields and API response schema.
5) Keep logs clean (no duplicate handlers). Avoid breaking UI.

Commands guidance:
- python -m venv .venv && .venv\Scripts\Activate.ps1
- pip install -r requirements.txt
- pip install pytest
- python scaffold.py
- pytest -q
- uvicorn app.main:app --reload
- streamlit run app/ui/app.py

Deliverables:
- Code per tasks
- Tests per tasks
- Passing test run transcript
- Short change log per task
```

## Successor Prompt (for the next engineering session)

```
You are entering as the successor engineer to implement the Universal Data Assistant scaffold into a runnable baseline with tests. Follow the Work Breakdown tasks U1–UI1 as specified below. Execute strictly in order, one task at a time.

Checklist for each task:
- Implement the function(s) named in the task.
- Add or update unit tests exactly as listed under that task.
- Run `pytest -q`; resolve failures until green.
- Update minimal docs in README if behavior changes (not expected for baseline).
- Ensure audit_trail updates include the fields stated.

Initial steps:
1) python scaffold.py
2) python -m venv .venv; .venv\Scripts\Activate.ps1
3) pip install -r requirements.txt
4) pip install pytest
5) pytest -q (expect all passing)

Implementation order:
- U1, U2, U3
- C1
- G1, G2
- N1, N2, N3, N4, N5, N6, N7, N8
- I1, I2
- X1, X2
- D1
- A1, A2
- UI1
- E2E1 and audit trail tests

Exit criteria:
- All tests pass
- API responds on /health and /chat with expected schema
- Streamlit UI runs and displays answer, citations, uncertainty, and validation
- Audit trail includes entries from all nodes with required fields
- No regressions against the suite
```

---

## Backlog Overview (Epics)
- Core Utilities and Config
- Graph Orchestration and State
- Retrieval and Answering Nodes
- Uncertainty, Validation, Auditor, Supervisor
- Ingestion and Indexing
- DLQ Infrastructure
- API and UI
- E2E and Governance

---

## Tasks Index and Order
Order of execution:
- U1 → U2 → U3 → C1 → G1 → G2 → N1 → N2 → N3 → N4 → N5 → N6 → N7 → N8 → I1 → I2 → X1 → X2 → D1 → A1 → A2 → UI1 → E2E1

---

## Task U1: app/utils/logging.setup_logging

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

## Task U2: app/utils/citations.format_citations

### Context
- Render evidence list into [idx] source :: heading strings.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Handle missing fields gracefully; maintain stable 1-based ordering.

### Unit Tests
- test_citations_basic: with heading and source_uri.
- test_citations_missing_fields: handle missing heading/source.

### Evaluation
- pytest -q -k citations

### Regression
- Deterministic ordering; format remains stable.

### Audit Artifacts
- Ensure audit_trail includes: N/A for utility

---

## Task U3: app/utils/uncertainty.entropy_from_logprobs and aggregate_uncertainty

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

## Task C1: app/config.Settings and AnswerPayload

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

## Task G1: app/graph/build_graph with fallback

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

## Task G2: app/graph/state.GraphState

### Context
- Typed state contract across nodes.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Provide TypedDict fields and use consistently across nodes.

### Unit Tests
- test_state_fields_presence: state after run contains expected keys.

### Evaluation
- pytest -q -k state

### Regression
- No key renames/removals.

### Audit Artifacts
- Ensure audit_trail includes: consistent keys used by nodes

---

## Task N1: router_node

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

## Task N2: retriever_node and simple_keyword_match

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

## Task N3: ranker_node

### Context
- Pass-through with future dedup/diversity.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Return evidence as-is; append audit with kept count.

### Unit Tests
- test_ranker_passthrough

### Evaluation
- pytest -q -k ranker

### Regression
- Maintain input ordering.

### Audit Artifacts
- Ensure audit_trail includes: node="ranker", kept

---

## Task N4: answerer_node

### Context
- Quote-first grounded answer and citations; abstain if no evidence.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Produce 'Q:' and 'A (grounded):' lines; include top-2 evidence lines and citations.

### Unit Tests
- test_answerer_with_evidence
- test_answerer_no_evidence

### Evaluation
- pytest -q -k answerer

### Regression
- No fabricated content; citation count matches evidence used.

### Audit Artifacts
- Ensure audit_trail includes: node="answerer", len

---

## Task N5: uncertainty_node

### Context
- Aggregate stub spans: low when evidence exists; high otherwise.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Set example span entropies and aggregate; append audit with overall.

### Unit Tests
- test_uncertainty_with_evidence_low
- test_uncertainty_without_evidence_high

### Evaluation
- pytest -q -k uncertainty_node

### Regression
- Uncertainty contains 'overall' and 'spans'.

### Audit Artifacts
- Ensure audit_trail includes: node="uncertainty", overall

---

## Task N6: validator_node

### Context
- Faithfulness = True if evidence found; else False.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Inspect retrieved_evidence and emit validation_reports; append audit.

### Unit Tests
- test_validator_faithful_with_evidence
- test_validator_unfaithful_without_evidence

### Evaluation
- pytest -q -k validator

### Regression
- validation_reports schema stable.

### Audit Artifacts
- Ensure audit_trail includes: node="validator", faithful

---

## Task N7: auditor_node

### Context
- Flag when high uncertainty or unfaithful.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Compute flag = (uncertainty.overall > 0.8) or (not faithful); append audit.

### Unit Tests
- test_auditor_flags_on_unfaithful
- test_auditor_not_flag_when_low_uncertainty_and_faithful

### Evaluation
- pytest -q -k auditor

### Regression
- Audit contains flag state.

### Audit Artifacts
- Ensure audit_trail includes: node="auditor", flag

---

## Task N8: supervisor_node

### Context
- Decision = 'answer' if faithful and low uncertainty else 'dlq' (stub).

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Append audit with decision; keep logic deterministic.

### Unit Tests
- test_supervisor_answers_when_confident
- test_supervisor_dlq_when_unfaithful

### Evaluation
- pytest -q -k supervisor

### Regression
- State includes 'decision'.

### Audit Artifacts
- Ensure audit_trail includes: node="supervisor", decision

---

## Task I1: ingestion.pipeline.normalize_document

### Context
- Decode bytes to text; produce document/sections structure.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Handle decoding errors with ignore; attach minimal metadata.

### Unit Tests
- test_normalize_document_basic

### Evaluation
- pytest -q -k normalize_document

### Regression
- Stable keys: document, sections, text.

### Audit Artifacts
- Ensure audit_trail includes: N/A for ingestion stub

---

## Task I2: ingestion.pipeline.batch_ingest

### Context
- Map normalize_document over inputs; maintain order.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Zip blobs and uris; return list of normalized docs.

### Unit Tests
- test_batch_ingest_lengths_match

### Evaluation
- pytest -q -k batch_ingest

### Regression
- Deterministic ordering.

### Audit Artifacts
- Ensure audit_trail includes: N/A for ingestion stub

---

## Task X1: indexing.chunking.simple_chunk_sections

### Context
- Split sections into fixed-size chunks; propagate metadata.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Chunk by max_len; include doc_id, source_uri, heading, hash.

### Unit Tests
- test_chunking_splits_text
- test_chunking_metadata_present

### Evaluation
- pytest -q -k chunking

### Regression
- No empty chunks; consistent chunk counts.

### Audit Artifacts
- Ensure audit_trail includes: N/A for indexing stub

---

## Task X2: indexing.vectorstore.LocalStore

### Context
- In-memory store with add and all returning copies.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Ensure all() returns a shallow copy to avoid external mutation.

### Unit Tests
- test_vectorstore_add_and_all

### Evaluation
- pytest -q -k vectorstore

### Regression
- No mutation leakage across calls.

### Audit Artifacts
- Ensure audit_trail includes: N/A for indexing stub

---

## Task D1: dlq.queue.FileDLQ.enqueue and stream

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

## Task A1: FastAPI /health

### Context
- Returns {status: ok} and 200.

### Acceptance Criteria
- All listed tests pass
- No regressions in related suites
- Audit trail entries updated where applicable

### Implementation
- Simple GET endpoint.

### Unit Tests
- test_health_endpoint

### Evaluation
- pytest -q -k health

### Regression
- Schema stable.

### Audit Artifacts
- Ensure audit_trail includes: N/A for health

---

## Task A2: FastAPI /chat

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

## Task UI1: Streamlit UI import and basic call

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

## Task E2E1: Smoke: build_graph().invoke returns draft_answer

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
