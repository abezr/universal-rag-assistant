#!/usr/bin/env python3
"""
Universal Data Assistant - Project Scaffolding Script

This script creates the full project structure and baseline implementation for the
Universal Data Assistant (UDA) architecture designed with LangGraph and optional
PydanticAI/SGR integrations.

Usage:
  python scaffold.py

After scaffolding:
  1) Create a virtual environment
  2) pip install -r requirements.txt
  3) Run the API: uvicorn app.main:app --reload
  4) (Optional) Run the UI: streamlit run app/ui/app.py

This scaffold is free-tier friendly: it includes a minimal runnable pipeline with
stubbed components and degrades gracefully if optional libraries are missing.
"""

import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent

FILES = {
    ".gitignore": textwrap.dedent(
        r"""
        __pycache__/
        *.pyc
        .env
        .venv/
        venv/
        .pytest_cache/
        .DS_Store
        .idea/
        .vscode/
        .mypy_cache/
        
        # Data
        data/
        storage/
        logs/
        
        # Streamlit
        .streamlit/
        
        # Build artifacts
        dist/
        build/
        *.egg-info/
        """.strip()
    ),
    "README.md": textwrap.dedent(
        r"""
        # Universal Data Assistant (UDA)
        
        Cooperative AI system for precise, cited Q&A over fuzzy internal documentation.
        Built with LangGraph (and optional PydanticAI/SGR), with uncertainty tracking,
        hallucination mitigation, citations, cross-validation, and DLQ-driven human-in-the-loop.
        
        ## Quickstart
        
        ```bash
        # 1) (optional) create virtualenv
        python -m venv .venv && .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
        
        # 2) install minimal dependencies
        pip install -r requirements.txt
        
        # 3) run API
        uvicorn app.main:app --reload
        
        # 4) (optional) run Streamlit UI in a second terminal
        streamlit run app/ui/app.py
        ```
        
        Visit http://127.0.0.1:8000/docs for API docs.
        
        ## Structure
        
        ```
        app/
          config.py            # Settings via Pydantic
          main.py              # FastAPI entrypoint
          graph/
            __init__.py
            state.py           # Typed state for graph
            nodes/
              __init__.py
              router.py
              retriever.py
              ranker.py
              answerer.py
              uncertainty.py
              validator.py
              auditor.py
              supervisor.py
          ingestion/
            __init__.py
            pipeline.py        # Normalization pipeline (stub)
            parsers.py         # Extractors (stub)
          indexing/
            __init__.py
            chunking.py        # Chunking strategies (stub)
            vectorstore.py     # Local store or stubs
          retrieval/
            __init__.py
            hybrid.py          # Hybrid retrieval (stub)
          validation/
            __init__.py
            nli.py             # NLI validator (stub)
          dlq/
            __init__.py
            queue.py           # Simple file-backed DLQ
          ui/
            __init__.py
            app.py             # Streamlit reference UI
          utils/
            __init__.py
            logging.py
            citations.py
            uncertainty.py
        tests/
          test_smoke.py
        requirements.txt            # Minimal deps
        requirements-optional.txt   # Optional deps for full features
        .env.example
        ```
        
        ## Notes
        - Minimal pipeline runs with only FastAPI, Pydantic and (optionally) LangGraph installed.
        - If LangGraph is not installed, the graph falls back to a simple sequential pipeline.
        - Optional retrieval/indexing/validator features are stubbed and can be turned on by installing
          extra dependencies in `requirements-optional.txt`.
        
        ## Environment
        Copy `.env.example` to `.env` and adjust values.
        
        ## License
        MIT (adjust as needed).
        """.strip()
    ),
    "requirements.txt": textwrap.dedent(
        r"""
        # Minimal runtime
        pydantic>=2.4
        fastapi>=0.110
        uvicorn[standard]>=0.23
        python-dotenv>=1.0
        
        # LangGraph (recommended)
        langgraph>=0.2.0
        
        # For UI (optional but lightweight)
        streamlit>=1.32
        """.strip()
    ),
    "requirements-optional.txt": textwrap.dedent(
        r"""
        # Retrieval / Embeddings / Reranking
        sentence-transformers>=2.2
        qdrant-client>=1.7
        lancedb>=0.5
        whoosh>=2.7
        scikit-learn>=1.3
        
        # Validation / NLI / Transformers
        transformers>=4.40
        torch>=2.1
        
        # Ingestion
        unstructured>=0.12
        pymupdf>=1.23
        pandas>=2.0
        python-docx>=1.1
        python-pptx>=0.6
        trafilatura>=1.6
        
        # Optional UI
        gradio>=4.0
        """.strip()
    ),
    ".env.example": textwrap.dedent(
        r"""
        # API
        API_HOST=127.0.0.1
        API_PORT=8000
        
        # Models
        PROVIDER=openai  # or local
        MODEL_NAME=gpt-4o-mini
        
        # Storage
        DATA_DIR=./data
        STORAGE_DIR=./storage
        DLQ_FILE=./storage/dlq.jsonl
        
        # Security / Tenancy
        DEFAULT_SECURITY_TAGS=public
        """.strip()
    ),
    "app/__init__.py": "",
    "app/config.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        import os
        from pydantic import BaseModel
        from pydantic_settings import BaseSettings, SettingsConfigDict
        
        class Settings(BaseSettings):
            api_host: str = os.getenv("API_HOST", "127.0.0.1")
            api_port: int = int(os.getenv("API_PORT", 8000))
            provider: str = os.getenv("PROVIDER", "local")
            model_name: str = os.getenv("MODEL_NAME", "stub-model")
            data_dir: str = os.getenv("DATA_DIR", "./data")
            storage_dir: str = os.getenv("STORAGE_DIR", "./storage")
            dlq_file: str = os.getenv("DLQ_FILE", "./storage/dlq.jsonl")
            default_security_tags: str = os.getenv("DEFAULT_SECURITY_TAGS", "public")
            
            model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
        
        settings = Settings()
        
        class AnswerPayload(BaseModel):
            answer: str
            citations: list[str] = []
            uncertainty: dict | None = None
            validation: dict | None = None
            decision: str = "answer"
        """.strip()
    ),
    "app/utils/__init__.py": "",
    "app/utils/logging.py": textwrap.dedent(
        r"""
        import logging
        import sys
        
        def setup_logging(level: int = logging.INFO) -> None:
            logger = logging.getLogger()
            if logger.handlers:
                return
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(level)
        """.strip()
    ),
    "app/utils/citations.py": textwrap.dedent(
        r"""
        from typing import List, Dict
        
        def format_citations(evidence: List[Dict]) -> list[str]:
            """Create simple citation strings from evidence items.
            Each evidence dict may include: {source_uri, heading, doc_id, score}
            """
            cites = []
            for idx, e in enumerate(evidence, start=1):
                src = e.get("source_uri") or e.get("doc_id", "unknown")
                heading = e.get("heading")
                frag = f"[{idx}] {src}"
                if heading:
                    frag += f" :: {heading}"
                cites.append(frag)
            return cites
        """.strip()
    ),
    "app/utils/uncertainty.py": textwrap.dedent(
        r"""
        from typing import List, Dict
        import math
        
        def entropy_from_logprobs(logprobs: List[float]) -> float:
            """Compute entropy given a list of log probabilities for top-k tokens."""
            probs = [math.exp(lp) for lp in logprobs]
            s = sum(probs)
            if s == 0:
                return 0.0
            probs = [p / s for p in probs]
            return -sum(p * math.log(p + 1e-12) for p in probs)
        
        def aggregate_uncertainty(spans: List[Dict]) -> Dict:
            """Aggregate span uncertainties to a simple summary.
            spans format: [{"start": int, "end": int, "entropy": float}]
            """
            if not spans:
                return {"overall": 0.0, "spans": []}
            overall = sum(s.get("entropy", 0.0) for s in spans) / max(len(spans), 1)
            return {"overall": overall, "spans": spans}
        """.strip()
    ),
    "app/graph/__init__.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any
        
        from .state import GraphState
        from .nodes.router import router_node
        from .nodes.retriever import retriever_node
        from .nodes.ranker import ranker_node
        from .nodes.answerer import answerer_node
        from .nodes.uncertainty import uncertainty_node
        from .nodes.validator import validator_node
        from .nodes.auditor import auditor_node
        from .nodes.supervisor import supervisor_node
        
        def build_graph():
            """Build the LangGraph if available; otherwise return a simple sequential pipeline."""
            try:
                from langgraph.graph import StateGraph, END
                sg = StateGraph(GraphState)
                sg.add_node("router", router_node)
                sg.add_node("retriever", retriever_node)
                sg.add_node("ranker", ranker_node)
                sg.add_node("answerer", answerer_node)
                sg.add_node("uncertainty", uncertainty_node)
                sg.add_node("validator", validator_node)
                sg.add_node("auditor", auditor_node)
                sg.add_node("supervisor", supervisor_node)
                
                sg.set_entry_point("router")
                sg.add_edge("router", "retriever")
                sg.add_edge("retriever", "ranker")
                sg.add_edge("ranker", "answerer")
                sg.add_edge("answerer", "uncertainty")
                sg.add_edge("uncertainty", "validator")
                sg.add_edge("validator", "auditor")
                sg.add_edge("auditor", "supervisor")
                sg.add_edge("supervisor", END)
                
                return sg.compile()
            except Exception:
                # Fallback sequential pipeline
                class SimplePipeline:
                    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
                        for node in (
                            router_node,
                            retriever_node,
                            ranker_node,
                            answerer_node,
                            uncertainty_node,
                            validator_node,
                            auditor_node,
                            supervisor_node,
                        ):
                            updates = node(state)
                            if updates:
                                state.update(updates)
                        return state
                return SimplePipeline()
        """.strip()
    ),
    "app/graph/state.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import List, Dict, Any, TypedDict
        
        class GraphState(TypedDict, total=False):
            user_query: str
            intent: str
            retrieved_evidence: List[Dict[str, Any]]
            draft_answer: str
            citations: List[str]
            uncertainty: Dict[str, Any]
            validation_reports: Dict[str, Any]
            decision: str
            audit_trail: List[Dict[str, Any]]
        """.strip()
    ),
    "app/graph/nodes/__init__.py": "",
    "app/graph/nodes/router.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any
        
        def router_node(state: Dict[str, Any]) -> Dict[str, Any]:
            q = (state.get("user_query") or "").lower()
            intent = "lookup"
            if any(k in q for k in ["why", "how", "compare", "design", "tradeoff"]):
                intent = "synthesis"
            if any(k in q for k in ["policy", "gdpr", "security", "compliance"]):
                intent = "policy"
            audit = state.get("audit_trail", [])
            audit.append({"node": "router", "intent": intent})
            return {"intent": intent, "audit_trail": audit}
        """.strip()
    ),
    "app/graph/nodes/retriever.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any, List
        
        # Minimal in-memory stub retrieval. Replace with real hybrid retrieval later.
        CORPUS = [
            {
                "doc_id": "doc-1",
                "heading": "UDA Overview",
                "text": "Universal Data Assistant provides precise, cited answers using RAG.",
                "source_uri": "internal://docs/uda/overview.md",
                "security_tags": ["public"],
            },
            {
                "doc_id": "doc-2",
                "heading": "Uncertainty Handling",
                "text": "UDA tracks token-level uncertainty via logprob entropy and span aggregation.",
                "source_uri": "internal://docs/uda/uncertainty.md",
                "security_tags": ["public"],
            },
        ]
        
        def simple_keyword_match(query: str, k: int = 3) -> List[dict]:
            if not query:
                return []
            terms = [t for t in query.lower().split() if len(t) > 2]
            scored = []
            for item in CORPUS:
                score = sum(item["text"].lower().count(t) for t in terms)
                if score > 0:
                    scored.append((score, item))
            scored.sort(reverse=True, key=lambda x: x[0])
            results = []
            for score, item in scored[:k]:
                r = dict(item)
                r["score"] = float(score)
                results.append(r)
            return results
        
        def retriever_node(state: Dict[str, Any]) -> Dict[str, Any]:
            query = state.get("user_query") or ""
            evidence = simple_keyword_match(query, k=5)
            audit = state.get("audit_trail", [])
            audit.append({"node": "retriever", "hits": len(evidence)})
            return {"retrieved_evidence": evidence, "audit_trail": audit}
        """.strip()
    ),
    "app/graph/nodes/ranker.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any
        
        def ranker_node(state: Dict[str, Any]) -> Dict[str, Any]:
            # Stub: assume retriever already scored documents reasonably
            ev = state.get("retrieved_evidence") or []
            # Could deduplicate and enforce diversity here
            audit = state.get("audit_trail", [])
            audit.append({"node": "ranker", "kept": len(ev)})
            return {"retrieved_evidence": ev, "audit_trail": audit}
        """.strip()
    ),
    "app/graph/nodes/answerer.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any
        from ...utils.citations import format_citations
        
        def answerer_node(state: Dict[str, Any]) -> Dict[str, Any]:
            query = state.get("user_query") or ""
            ev = state.get("retrieved_evidence") or []
            if not ev:
                draft = (
                    "I don't have enough information to answer confidently. "
                    "Please provide more details or ingest relevant documents."
                )
                citations = []
            else:
                # Simple grounded answer: quote evidence and cite
                lines = [f"Q: {query}", "A (grounded):"]
                for i, e in enumerate(ev[:2], start=1):
                    lines.append(f"- {e.get('text')}")
                draft = "\n".join(lines)
                citations = format_citations(ev[:2])
            audit = state.get("audit_trail", [])
            audit.append({"node": "answerer", "len": len(draft)})
            return {"draft_answer": draft, "citations": citations, "audit_trail": audit}
        """.strip()
    ),
    "app/graph/nodes/uncertainty.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any
        from ...utils.uncertainty import aggregate_uncertainty
        
        def uncertainty_node(state: Dict[str, Any]) -> Dict[str, Any]:
            # Stub: no real logprobs available in the minimal scaffold.
            # Simulate higher confidence if there is evidence, lower otherwise.
            ev = state.get("retrieved_evidence") or []
            if ev:
                spans = [{"start": 0, "end": 10, "entropy": 0.1}]
            else:
                spans = [{"start": 0, "end": 10, "entropy": 1.2}]
            unc = aggregate_uncertainty(spans)
            audit = state.get("audit_trail", [])
            audit.append({"node": "uncertainty", "overall": unc.get("overall")})
            return {"uncertainty": unc, "audit_trail": audit}
        """.strip()
    ),
    "app/graph/nodes/validator.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any
        
        def validator_node(state: Dict[str, Any]) -> Dict[str, Any]:
            # Stub: mark as faithful if evidence exists.
            ev = state.get("retrieved_evidence") or []
            faithful = bool(ev)
            report = {"faithful": faithful, "checks": ["stub"]}
            audit = state.get("audit_trail", [])
            audit.append({"node": "validator", "faithful": faithful})
            return {"validation_reports": report, "audit_trail": audit}
        """.strip()
    ),
    "app/graph/nodes/auditor.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any
        
        def auditor_node(state: Dict[str, Any]) -> Dict[str, Any]:
            # Stub: cross-validate by simple heuristics
            unc = (state.get("uncertainty") or {}).get("overall", 1.0)
            faithful = (state.get("validation_reports") or {}).get("faithful", False)
            flag = (unc > 0.8) or (not faithful)
            audit = state.get("audit_trail", [])
            audit.append({"node": "auditor", "flag": flag})
            return {"audit_trail": audit}
        """.strip()
    ),
    "app/graph/nodes/supervisor.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any
        
        def supervisor_node(state: Dict[str, Any]) -> Dict[str, Any]:
            unc = (state.get("uncertainty") or {}).get("overall", 1.0)
            faithful = (state.get("validation_reports") or {}).get("faithful", False)
            if faithful and unc < 0.8:
                decision = "answer"
            else:
                # In a full implementation, route to DLQ or ask clarification
                decision = "answer" if faithful else "dlq"
            audit = state.get("audit_trail", [])
            audit.append({"node": "supervisor", "decision": decision})
            return {"decision": decision, "audit_trail": audit}
        """.strip()
    ),
    "app/ingestion/__init__.py": "",
    "app/ingestion/pipeline.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any, List
        
        def normalize_document(blob: bytes, source_uri: str) -> Dict[str, Any]:
            # Stub normalization: returns a simple section
            text = blob.decode(errors="ignore")
            return {
                "document": {
                    "id": source_uri,
                    "type": "text/plain",
                    "source_uri": source_uri,
                },
                "sections": [
                    {"id": f"{source_uri}#0", "heading": None, "text": text, "metadata": {}}
                ],
            }
        
        def batch_ingest(blobs: List[bytes], uris: List[str]) -> List[Dict[str, Any]]:
            return [normalize_document(b, u) for b, u in zip(blobs, uris)]
        """.strip()
    ),
    "app/ingestion/parsers.py": textwrap.dedent(
        r"""
        # Placeholders for PDF/DOCX/HTML parsers using free-tier libs (PyMuPDF, python-docx, trafilatura, etc.)
        # Implement as needed.
        """.strip()
    ),
    "app/indexing/__init__.py": "",
    "app/indexing/chunking.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import Dict, Any, List
        
        def simple_chunk_sections(doc: Dict[str, Any], max_len: int = 400) -> List[Dict[str, Any]]:
            chunks: List[Dict[str, Any]] = []
            for sec in doc.get("sections", []):
                text = sec.get("text", "")
                for i in range(0, len(text), max_len):
                    part = text[i:i+max_len]
                    chunks.append({
                        "doc_id": doc["document"]["id"],
                        "heading": sec.get("heading"),
                        "text": part,
                        "source_uri": doc["document"]["source_uri"],
                        "hash": hash(part),
                    })
            return chunks
        """.strip()
    ),
    "app/indexing/vectorstore.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from typing import List, Dict, Any
        
        # A trivial in-memory vector/sparse store stand-in
        class LocalStore:
            def __init__(self) -> None:
                self._data: List[Dict[str, Any]] = []
            
            def add(self, items: List[Dict[str, Any]]) -> None:
                self._data.extend(items)
            
            def all(self) -> List[Dict[str, Any]]:
                return list(self._data)
        
        STORE = LocalStore()
        """.strip()
    ),
    "app/retrieval/__init__.py": "",
    "app/retrieval/hybrid.py": textwrap.dedent(
        r"""
        # Placeholder for hybrid retrieval combining vector and BM25; see retriever node for stub.
        """.strip()
    ),
    "app/validation/__init__.py": "",
    "app/validation/nli.py": textwrap.dedent(
        r"""
        # Stub for NLI/faithfulness checks using transformers or lightweight models.
        """.strip()
    ),
    "app/dlq/__init__.py": "",
    "app/dlq/queue.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        import json
        from typing import Dict, Any, Optional
        from pathlib import Path
        
        class FileDLQ:
            def __init__(self, path: str) -> None:
                self.path = Path(path)
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.path.touch(exist_ok=True)
            
            def enqueue(self, item: Dict[str, Any]) -> None:
                with self.path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
            def stream(self):
                with self.path.open("r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            yield json.loads(line)
        """.strip()
    ),
    "app/ui/__init__.py": "",
    "app/ui/app.py": textwrap.dedent(
        r"""
        import streamlit as st
        from app.graph import build_graph
        
        st.set_page_config(page_title="Universal Data Assistant", layout="wide")
        st.title("Universal Data Assistant (UDA)")
        
        if "graph" not in st.session_state:
            st.session_state.graph = build_graph()
        
        user_query = st.text_input("Ask a question about your docs:")
        if st.button("Ask") and user_query:
            res = st.session_state.graph.invoke({"user_query": user_query})
            st.subheader("Answer")
            st.write(res.get("draft_answer", ""))
            
            cites = res.get("citations") or []
            if cites:
                st.subheader("Citations")
                for c in cites:
                    st.write(f"- {c}")
            
            unc = res.get("uncertainty") or {}
            st.subheader("Uncertainty")
            st.json(unc)
            
            val = res.get("validation_reports") or {}
            st.subheader("Validation")
            st.json(val)
        """.strip()
    ),
    "app/main.py": textwrap.dedent(
        r"""
        from __future__ import annotations
        from fastapi import FastAPI
        from pydantic import BaseModel
        from app.config import settings, AnswerPayload
        from app.utils.logging import setup_logging
        from app.graph import build_graph
        
        setup_logging()
        app = FastAPI(title="Universal Data Assistant")
        graph = build_graph()
        
        class ChatRequest(BaseModel):
            message: str
        
        @app.get("/health")
        def health():
            return {"status": "ok"}
        
        @app.post("/chat", response_model=AnswerPayload)
        def chat(req: ChatRequest):
            state = graph.invoke({"user_query": req.message})
            return AnswerPayload(
                answer=state.get("draft_answer", ""),
                citations=state.get("citations", []),
                uncertainty=state.get("uncertainty"),
                validation=state.get("validation_reports"),
                decision=state.get("decision", "answer"),
            )
        """.strip()
    ),
    "tests/__init__.py": "",
    "tests/test_smoke.py": textwrap.dedent(
        r"""
        from app.graph import build_graph
        
        def test_graph_smoke():
            g = build_graph()
            out = g.invoke({"user_query": "How does UDA handle uncertainty?"})
            assert "draft_answer" in out
        """.strip()
    ),
}

# Additional dependency for pydantic-settings used in config.py
# Add it inline here to avoid missing import after scaffold
FILES["requirements.txt"] += "\npydantic-settings>=2.0\n"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def main():
    for rel, content in FILES.items():
        write_file(ROOT / rel, content)
    # Create placeholder dirs that may be ignored by git
    for d in (ROOT / "data", ROOT / "storage", ROOT / "logs"):
        d.mkdir(parents=True, exist_ok=True)
    print("Scaffold created successfully. Key files:")
    for rel in ["README.md", "requirements.txt", "app/main.py", "app/graph/__init__.py", "app/ui/app.py"]:
        print(" -", rel)


if __name__ == "__main__":
    main()
