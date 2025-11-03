#!/usr/bin/env python3
"""
Generates documentation files for the Universal Data Assistant implementation plan:
- Implementation plan (docs/IMPLEMENTATION_PLAN.md)
- Granular tasks (docs/tasks/*.md)
- Regression suites summary (docs/REGRESSION_SUITES.md)
- Orchestrator and successor prompts (docs/prompts/*.txt)

Usage:
  python tasks_scaffold.py

This script is idempotent and will overwrite existing files with the same names.
"""

from pathlib import Path
import textwrap

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
TASKS_DIR = DOCS / "tasks"
PROMPTS_DIR = DOCS / "prompts"

IMPLEMENTATION_PLAN = textwrap.dedent(
    r"""
    # Universal Data Assistant — Implementation Plan

    Pre-flight baseline
    - Run: `python scaffold.py`
    - Create venv and install deps: `python -m venv .venv && .venv/Scripts/Activate.ps1`; `pip install -r requirements.txt`; `pip install pytest`
    - Run tests: `pytest -q` (initially passing)
    - Start API: `uvicorn app.main:app --reload` and verify `/health`

    Global audit and governance expectations
    - Every graph node appends to audit_trail in state: `{node, info...}`
    - Decisions and routing recorded: intent, evidence count, validation results, uncertainty score, final decision
    - DLQ items contain full envelope (reason_code, artifacts) when applicable
    - Prompts, model IDs, parameters, and citations are traceable in audit trail (stubbed initially; full fidelity later)

    Phased execution order
    - Phase 0: Scaffold and baseline run
    - Phase 1: Core utilities and config (U1–U3, C1)
    - Phase 2: Graph/build/state (G1–G2)
    - Phase 3: Node implementations (N1–N8)
    - Phase 4: Ingestion and indexing (I1–I2, X1–X2)
    - Phase 5: DLQ (D1)
    - Phase 6: API and UI (A1–A2, UI1)
    - Phase 7: E2E smoke and stabilization (E2E1)

    Evaluation and regression
    - For each task, add unit tests and run: `pytest -q -k <scope>`
    - API smoke: `uvicorn app.main:app --reload` then GET `/health`, POST `/chat`
    - UI smoke: `streamlit run app/ui/app.py`
    - Maintain regression: do not break audit trail schema or API response model

    Exit criteria
    - All tests pass
    - `/health` returns `{ "status": "ok" }`
    - `/chat` returns AnswerPayload schema
    - Streamlit UI renders and answers with citations, uncertainty, validation
    - Audit trail includes entries from all nodes
    - No duplicate log handlers; no regressions against suite
    """
)

REGRESSION_SUITES = textwrap.dedent(
    r"""
    # Universal Data Assistant — Regression Suites Summary

    Core regression suites
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

    Contract stability tests
    - tests/test_api_contract.py: verify /chat and /health contracts
    - tests/test_audit_trail.py: presence and order of node audit entries
    - tests/test_decision_policy.py: supervisor decisions by scenario

    Command checklist per change
    - Run: `pytest -q`
    - If API touched: manual `/health` and `/chat` checks
    - If UI touched: import app.ui.app in a Python REPL and ensure no ImportError
    """
)

ORCHESTRATOR_PROMPT = textwrap.dedent(
    r"""
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
    2) Implement tasks U1–UI1 in the defined order.
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
    """
)

SUCCESSOR_PROMPT = textwrap.dedent(
    r"""
    You are entering as the successor engineer to implement the Universal Data Assistant scaffold into a runnable baseline with tests. Follow the Work Breakdown tasks U1–UI1 as specified in the docs/tasks directory. Execute strictly in order, one task at a time.

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
    """
)

# Define tasks
TASKS = [
    {
        "id": "U1",
        "title": "app/utils/logging.setup_logging",
        "context": "Initialize root logger once with stdout handler and deterministic format.",
        "implementation": "Create a function that sets up logging only once. Prevent duplicate handlers across multiple imports/requests.",
        "tests": [
            "test_logging_idempotent: calling setup_logging twice does not add duplicate handlers.",
            "test_logging_format: emitted line matches '%(asctime)s | %(levelname)s | %(name)s | %(message)s' (regex).",
        ],
        "evaluation": "pytest -q -k logging",
        "regression": "No duplicate logs across API requests; format unchanged.",
    },
    {
        "id": "U2",
        "title": "app/utils/citations.format_citations",
        "context": "Render evidence list into [idx] source :: heading strings.",
        "implementation": "Handle missing fields gracefully; maintain stable 1-based ordering.",
        "tests": [
            "test_citations_basic: with heading and source_uri.",
            "test_citations_missing_fields: handle missing heading/source.",
        ],
        "evaluation": "pytest -q -k citations",
        "regression": "Deterministic ordering; format remains stable.",
    },
    {
        "id": "U3",
        "title": "app/utils/uncertainty.entropy_from_logprobs and aggregate_uncertainty",
        "context": "Entropy computation and aggregation of span uncertainties.",
        "implementation": "Compute entropy from logprobs; aggregate spans to overall average; safe on empty.",
        "tests": [
            "test_entropy_monotonicity: flatter distributions => higher entropy.",
            "test_aggregate_empty: returns overall 0.0.",
            "test_aggregate_average: correct averaging across spans.",
        ],
        "evaluation": "pytest -q -k uncertainty",
        "regression": "No negative entropy; no division-by-zero.",
    },
    {
        "id": "C1",
        "title": "app/config.Settings and AnswerPayload",
        "context": "Settings management and API response schema.",
        "implementation": "Use pydantic-settings to read .env; AnswerPayload includes answer, citations, uncertainty, validation, decision.",
        "tests": [
            "test_settings_env_override: env vars override defaults.",
            "test_answer_payload_schema: serialization/deserialization round-trip.",
        ],
        "evaluation": "pytest -q -k settings",
        "regression": "Do not rename keys; preserve defaults.",
    },
    {
        "id": "G1",
        "title": "app/graph/build_graph with fallback",
        "context": "Graph builds using LangGraph if present; otherwise uses sequential pipeline.",
        "implementation": "Try import; on failure, provide SimplePipeline.invoke calling nodes in order.",
        "tests": [
            "test_graph_builds_without_langgraph: simulate import error and verify pipeline.",
            "test_graph_invocation_flow: audit_trail contains all nodes in order.",
        ],
        "evaluation": "pytest -q -k graph",
        "regression": "Resilient build path; do not break if LangGraph missing.",
    },
    {
        "id": "G2",
        "title": "app/graph/state.GraphState",
        "context": "Typed state contract across nodes.",
        "implementation": "Provide TypedDict fields and use consistently across nodes.",
        "tests": [
            "test_state_fields_presence: state after run contains expected keys.",
        ],
        "evaluation": "pytest -q -k state",
        "regression": "No key renames/removals.",
    },
    {
        "id": "N1",
        "title": "router_node",
        "context": "Intent classification and audit append.",
        "implementation": "Classify lookup/synthesis/policy by keywords; append audit entry with intent.",
        "tests": [
            "test_router_synthesis_intent",
            "test_router_policy_intent",
            "test_router_default_lookup",
        ],
        "evaluation": "pytest -q -k router",
        "regression": "Default remains 'lookup'.",
    },
    {
        "id": "N2",
        "title": "retriever_node and simple_keyword_match",
        "context": "Stub retrieval over in-memory corpus; audit hits count.",
        "implementation": "Tokenize query; count term occurrences; sort desc by score; include metadata.",
        "tests": [
            "test_retriever_hits",
            "test_retriever_scores_sorted",
            "test_retriever_empty_query",
        ],
        "evaluation": "pytest -q -k retriever",
        "regression": "Return items include score, source_uri, doc_id.",
    },
    {
        "id": "N3",
        "title": "ranker_node",
        "context": "Pass-through with future dedup/diversity.",
        "implementation": "Return evidence as-is; append audit with kept count.",
        "tests": [
            "test_ranker_passthrough",
        ],
        "evaluation": "pytest -q -k ranker",
        "regression": "Maintain input ordering.",
    },
    {
        "id": "N4",
        "title": "answerer_node",
        "context": "Quote-first grounded answer and citations; abstain if no evidence.",
        "implementation": "Produce 'Q:' and 'A (grounded):' lines; include top-2 evidence lines and citations.",
        "tests": [
            "test_answerer_with_evidence",
            "test_answerer_no_evidence",
        ],
        "evaluation": "pytest -q -k answerer",
        "regression": "No fabricated content; citation count matches evidence used.",
    },
    {
        "id": "N5",
        "title": "uncertainty_node",
        "context": "Aggregate stub spans: low when evidence exists; high otherwise.",
        "implementation": "Set example span entropies and aggregate; append audit with overall.",
        "tests": [
            "test_uncertainty_with_evidence_low",
            "test_uncertainty_without_evidence_high",
        ],
        "evaluation": "pytest -q -k uncertainty_node",
        "regression": "Uncertainty contains 'overall' and 'spans'.",
    },
    {
        "id": "N6",
        "title": "validator_node",
        "context": "Faithfulness = True if evidence found; else False.",
        "implementation": "Inspect retrieved_evidence and emit validation_reports; append audit.",
        "tests": [
            "test_validator_faithful_with_evidence",
            "test_validator_unfaithful_without_evidence",
        ],
        "evaluation": "pytest -q -k validator",
        "regression": "validation_reports schema stable.",
    },
    {
        "id": "N7",
        "title": "auditor_node",
        "context": "Flag when high uncertainty or unfaithful.",
        "implementation": "Compute flag = (uncertainty.overall > 0.8) or (not faithful); append audit.",
        "tests": [
            "test_auditor_flags_on_unfaithful",
            "test_auditor_not_flag_when_low_uncertainty_and_faithful",
        ],
        "evaluation": "pytest -q -k auditor",
        "regression": "Audit contains flag state.",
    },
    {
        "id": "N8",
        "title": "supervisor_node",
        "context": "Decision = 'answer' if faithful and low uncertainty else 'dlq' (stub).",
        "implementation": "Append audit with decision; keep logic deterministic.",
        "tests": [
            "test_supervisor_answers_when_confident",
            "test_supervisor_dlq_when_unfaithful",
        ],
        "evaluation": "pytest -q -k supervisor",
        "regression": "State includes 'decision'.",
    },
    {
        "id": "I1",
        "title": "ingestion.pipeline.normalize_document",
        "context": "Decode bytes to text; produce document/sections structure.",
        "implementation": "Handle decoding errors with ignore; attach minimal metadata.",
        "tests": [
            "test_normalize_document_basic",
        ],
        "evaluation": "pytest -q -k normalize_document",
        "regression": "Stable keys: document, sections, text.",
    },
    {
        "id": "I2",
        "title": "ingestion.pipeline.batch_ingest",
        "context": "Map normalize_document over inputs; maintain order.",
        "implementation": "Zip blobs and uris; return list of normalized docs.",
        "tests": [
            "test_batch_ingest_lengths_match",
        ],
        "evaluation": "pytest -q -k batch_ingest",
        "regression": "Deterministic ordering.",
    },
    {
        "id": "X1",
        "title": "indexing.chunking.simple_chunk_sections",
        "context": "Split sections into fixed-size chunks; propagate metadata.",
        "implementation": "Chunk by max_len; include doc_id, source_uri, heading, hash.",
        "tests": [
            "test_chunking_splits_text",
            "test_chunking_metadata_present",
        ],
        "evaluation": "pytest -q -k chunking",
        "regression": "No empty chunks; consistent chunk counts.",
    },
    {
        "id": "X2",
        "title": "indexing.vectorstore.LocalStore",
        "context": "In-memory store with add and all returning copies.",
        "implementation": "Ensure all() returns a shallow copy to avoid external mutation.",
        "tests": [
            "test_vectorstore_add_and_all",
        ],
        "evaluation": "pytest -q -k vectorstore",
        "regression": "No mutation leakage across calls.",
    },
    {
        "id": "D1",
        "title": "dlq.queue.FileDLQ.enqueue and stream",
        "context": "Append-only JSONL with safe directory creation.",
        "implementation": "On init create directories; enqueue writes JSONL; stream yields parsed lines.",
        "tests": [
            "test_dlq_enqueue_and_stream",
        ],
        "evaluation": "pytest -q -k dlq",
        "regression": "No invalid JSON; preserves insertion order.",
    },
    {
        "id": "A1",
        "title": "FastAPI /health",
        "context": "Returns {status: ok} and 200.",
        "implementation": "Simple GET endpoint.",
        "tests": [
            "test_health_endpoint",
        ],
        "evaluation": "pytest -q -k health",
        "regression": "Schema stable.",
    },
    {
        "id": "A2",
        "title": "FastAPI /chat",
        "context": "Accepts message; invokes graph; returns AnswerPayload.",
        "implementation": "Pydantic request model; call graph.invoke; adapt fields.",
        "tests": [
            "test_chat_endpoint_basic",
            "test_chat_abstain_when_no_hits",
        ],
        "evaluation": "pytest -q -k chat",
        "regression": "Keys stable: answer, citations, uncertainty, validation, decision.",
    },
    {
        "id": "UI1",
        "title": "Streamlit UI import and basic call",
        "context": "Headless import works; manual run displays sections.",
        "implementation": "Use build_graph and display answer/citations/uncertainty/validation.",
        "tests": [
            "test_streamlit_import_succeeds",
        ],
        "evaluation": "pytest -q -k streamlit_import (import-only)",
        "regression": "No import-time side effects.",
    },
    {
        "id": "E2E1",
        "title": "Smoke: build_graph().invoke returns draft_answer",
        "context": "End-to-end minimal graph invocation.",
        "implementation": "Keep tests/tests_smoke.py green with current scaffold.",
        "tests": [
            "test_graph_smoke",
        ],
        "evaluation": "pytest -q -k smoke",
        "regression": "Always pass regardless of LangGraph presence.",
    },
]


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_plan_files():
    write_file(DOCS / "IMPLEMENTATION_PLAN.md", IMPLEMENTATION_PLAN)
    write_file(DOCS / "REGRESSION_SUITES.md", REGRESSION_SUITES)
    write_file(PROMPTS_DIR / "orchestrator_prompt.txt", ORCHESTRATOR_PROMPT)
    write_file(PROMPTS_DIR / "successor_prompt.txt", SUCCESSOR_PROMPT)


def write_tasks_files():
    index_lines = ["# UDA Tasks Index", "", "Order of execution:"]
    order = [
        "U1", "U2", "U3", "C1", "G1", "G2",
        "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8",
        "I1", "I2", "X1", "X2", "D1", "A1", "A2", "UI1", "E2E1",
    ]
    index_lines.append("- " + " → ".join(order))
    index_lines.append("")
    for t in TASKS:
        fname = f"{t['id']}_{t['title'].split('.')[-1].replace(' ', '_')}.md"
        path = TASKS_DIR / fname
        content = textwrap.dedent(
            f"""
            # Task {t['id']}: {t['title']}

            Context
            - {t['context']}

            Acceptance Criteria
            - All listed tests pass
            - No regressions in related suites
            - Audit trail entries updated where applicable

            Implementation
            - {t['implementation']}

            Unit Tests
            - """.rstrip()
        )
        for test in t["tests"]:
            content += f"\n  - {test}"
        content += textwrap.dedent(
            f"""

            Evaluation
            - {t['evaluation']}

            Regression
            - {t['regression']}

            Audit Artifacts
            - Ensure audit_trail includes: node name and key fields for this step (if applicable)
            """
        )
        write_file(path, content)
        index_lines.append(f"- [{t['id']}: {t['title']}]({fname})")
    write_file(TASKS_DIR / "README.md", "\n".join(index_lines))


def main():
    write_plan_files()
    write_tasks_files()
    print("Task docs created:")
    print(" - docs/IMPLEMENTATION_PLAN.md")
    print(" - docs/REGRESSION_SUITES.md")
    print(" - docs/prompts/orchestrator_prompt.txt")
    print(" - docs/prompts/successor_prompt.txt")
    print(" - docs/tasks/*.md and docs/tasks/README.md")


if __name__ == "__main__":
    main()
