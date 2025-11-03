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
- [U1: app/utils/logging.setup_logging](docs/tasks/U1-app-utils-logging-setup-logging.md)
- [U2: app/utils/citations.format_citations](docs/tasks/U2-app-utils-citations-format-citations.md)
- [U3: app/utils/uncertainty.entropy_from_logprobs and aggregate_uncertainty](docs/tasks/U3-app-utils-uncertainty-entropy-from-logprobs-and-aggregate-uncertainty.md)
- [C1: app/config.Settings and AnswerPayload](docs/tasks/C1-app-config-Settings-and-AnswerPayload.md)
- [G1: app/graph/build_graph with fallback](docs/tasks/G1-app-graph-build-graph-with-fallback.md)
- [G2: app/graph/state.GraphState](docs/tasks/G2-app-graph-state-GraphState.md)
- [N1: router_node](docs/tasks/N1-router-node.md)
- [N2: retriever_node and simple_keyword_match](docs/tasks/N2-retriever-node-and-simple-keyword-match.md)
- [N3: ranker_node](docs/tasks/N3-ranker-node.md)
- [N4: answerer_node](docs/tasks/N4-answerer-node.md)
- [N5: uncertainty_node](docs/tasks/N5-uncertainty-node.md)
- [N6: validator_node](docs/tasks/N6-validator-node.md)
- [N7: auditor_node](docs/tasks/N7-auditor-node.md)
- [N8: supervisor_node](docs/tasks/N8-supervisor-node.md)
- [I1: ingestion.pipeline.normalize_document](docs/tasks/I1-ingestion-pipeline-normalize-document.md)
- [I2: ingestion.pipeline.batch_ingest](docs/tasks/I2-ingestion-pipeline-batch-ingest.md)
- [X1: indexing.chunking.simple_chunk_sections](docs/tasks/X1-indexing-chunking-simple-chunk-sections.md)
- [X2: indexing.vectorstore.LocalStore](docs/tasks/X2-indexing-vectorstore-LocalStore.md)
- [D1: dlq.queue.FileDLQ.enqueue and stream](docs/tasks/D1-dlq-queue-FileDLQ-enqueue-and-stream.md)
- [A1: FastAPI /health](docs/tasks/A1-FastAPI-health.md)
- [A2: FastAPI /chat](docs/tasks/A2-FastAPI-chat.md)
- [UI1: Streamlit UI import and basic call](docs/tasks/UI1-Streamlit-UI-import-and-basic-call.md)
- [E2E1: Smoke: build_graph().invoke returns draft_answer](docs/tasks/E2E1-Smoke-build-graph-invoke-returns-draft-answer.md)
