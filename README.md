# ReviewMate

> Automate the first-pass of any literature review.

ReviewMate ingests a research question and produces a structured synthesis from open-access academic papers — combining a fine-tuned DistilBERT classifier for abstract structure, multi-agent orchestration via LangGraph, and parallel paper fetching from arXiv, Semantic Scholar, OpenAlex, and PubMed.

**Status:** 🚧 Under active development (Phase 0 of 6).

---

## Why this project

Manual literature review for any research topic means scanning 500+ papers — infeasible for an individual researcher starting in a new area. Existing tools (Elicit, Consensus) are paywalled or generic. ReviewMate exists to provide a free, transparent, open-source alternative for **first-pass synthesis** — not a replacement for systematic review.

---

## What it does

Given a research question, ReviewMate:

1. Decomposes the query into searchable sub-questions
2. Fetches papers in parallel from arXiv, Semantic Scholar, OpenAlex, and PubMed
3. Deduplicates across sources
4. Filters by semantic relevance
5. Classifies each abstract sentence (Background / Objective / Methods / Results / Conclusions) using a **fine-tuned DistilBERT** on PubMed-RCT-200k
6. Extracts contributions and limitations
7. Synthesizes a narrative literature review with inline citations

---

## Architecture

_Will be added: Mermaid diagram showing LangGraph workflow._

---

## What is explicitly out of scope

- ❌ Paywalled full text (Elsevier, Springer). Open-access abstracts + full text only.
- ❌ Sci-Hub or grey-zone scraping.
- ❌ PRISMA-compliant systematic review (risk of bias scoring, meta-analysis). This is **first-pass** synthesis.
- ❌ Multi-user authentication. Single-user tool.

Best coverage in STEM and biomedical fields. Humanities and non-English research may have limited results due to upstream API coverage.

---

## Tech stack

| Layer | Choice |
|---|---|
| Backend | FastAPI |
| Orchestration | LangGraph |
| Frontend | Streamlit |
| LLM (synthesis) | Groq + Llama 3.3 70B |
| Fine-tuned classifier | DistilBERT (PubMed-RCT-200k) |
| Paper APIs | arXiv, Semantic Scholar, OpenAlex, PubMed |
| Training compute | Kaggle Notebooks (free GPU) |
| Container | Docker + docker-compose |
| Deployment | Streamlit Cloud / HuggingFace Spaces |
| CI/CD | GitHub Actions |
| Testing | pytest + ruff |

---

## Setup

_Will be added once Phase 0 is complete._

---

## Usage

_Will be added once Phase 4 is complete._

---

## Evaluation

_Will be added once Phase 1 fine-tuning is complete (per-class precision/recall/F1, confusion matrix)._

---

## Roadmap

- [x] Phase 0 — Setup and grounding
- [ ] Phase 1 — Fine-tune DistilBERT on PubMed-RCT-200k
- [ ] Phase 2 — Paper fetchers (arXiv, S2, OpenAlex, PubMed)
- [ ] Phase 3 — LangGraph workflow
- [ ] Phase 4 — Streamlit UI + FastAPI wiring
- [ ] Phase 5 — Production hardening + deployment

---

## License

MIT