# ReviewMate — Design Document

**Author:** Himel Das  
**Status:** Phase 0 (Setup and grounding)  
**Last updated:** 2026-06-24

---

## Problem

A researcher starting work in a new area faces 500+ relevant papers per question. Manually scanning all of them is infeasible. Existing tools are either paywalled (Elicit, Consensus) or generic (ChatGPT). No open-source tool exists that:

- Fetches from multiple academic sources in parallel
- Structures abstracts at the sentence level
- Synthesizes findings into a coherent narrative with citations
- Runs entirely on free infrastructure

ReviewMate fills this gap for **first-pass** synthesis. It is not a replacement for systematic review.

---

## Users

A single researcher (initially the author, for PhD application literature reviews). Designed to be domain-agnostic but with strongest coverage in STEM and biomedical fields due to upstream API characteristics.

---

## Inputs and outputs

**Input (from Streamlit UI):**
- Research question (free text)
- Year range (user-selected, e.g. 2020–2026)
- Max papers to retrieve (10 / 30 / 50)
- Source toggles (arXiv, S2, OpenAlex, PubMed)

**Output (rendered in Streamlit):**
1. Synthesized narrative — dominant methods, consensus, conflicts, gaps (woven in)
2. Per-paper structured cards — Background / Objective / Methods / Results / Conclusions
3. Sortable paper table — Title, Authors, Year, Citations, DOI, PDF
4. Downloadable BibTeX references

---

## Architecture

User Research Question (Streamlit UI)
            │
            ▼
    FastAPI Backend
            │
            ▼
    LangGraph Workflow:
        1. Query Decomposer        (Groq Llama 3.3 70B)
        2. Paper Fetcher (parallel) (arXiv / S2 / OpenAlex / PubMed)
        3. Deduplicator            (DOI + normalized title)
        4. Relevance Filter        (sentence-transformers)
        5. Abstract Parser         (fine-tuned DistilBERT)
        6. Contribution Extractor  (Groq Llama 3.3 70B)
        7. Synthesizer             (Groq Llama 3.3 70B)
            │
            ▼
    Structured Report (4 sections)

---

## Key technical choices

| Decision | Choice | Reasoning |
|---|---|---|
| Orchestration | LangGraph | Multi-step + parallel + conditional workflow needs explicit graph |
| Classifier | DistilBERT (66M) fine-tuned on PubMed-RCT-200k | Small enough for 8GB RAM inference, free Kaggle GPU for training |
| LLM | Groq Llama 3.3 70B | Free tier, fast, already integrated from MediQuery |
| Frontend | Streamlit | New stack for portfolio diversity; Next.js overkill for single-page tool |
| Hosting | Streamlit Cloud / HF Spaces | Free, sufficient for portfolio demo |

---

## Out of scope

- Paywalled full text (Elsevier, Springer)
- Grey-zone scraping (Sci-Hub)
- PRISMA-compliant systematic review
- Multi-user authentication
- Real-time paper alerts
- Number-aware count statistics (references list shows count implicitly)

---

## Honest limitations

1. **LLM-generated synthesis is hallucination-prone.** Surfaced gaps and conflicts are starting hypotheses, not validated claims. Manual verification required.
2. **Coverage is API-bound.** Humanities and non-English research will have limited results because upstream APIs cover them poorly.
3. **Fine-tuned classifier is biomedical-trained.** Sentence classification may degrade on non-biomedical abstracts (acceptable for a portfolio first version; cross-domain fine-tuning is future work).

---

## Phase plan

| Phase | Focus | Duration |
|---|---|---|
| 0 | Setup, scoping, design doc | 2–3 days |
| 1 | Fine-tune DistilBERT on PubMed-RCT-200k (Kaggle) | 4–5 days |
| 2 | Paper fetchers (4 APIs) + aggregator | 3–4 days |
| 3 | LangGraph workflow assembly | 5–6 days |
| 4 | Streamlit UI + FastAPI wiring | 3–4 days |
| 5 | Docker + tests + CI/CD + deployment | 3–4 days |

## Phase 1: Rhetorical Sentence Classifier (Completed)

A DistilBERT-based classifier trained via two-stage transfer learning to categorize sentences from research abstracts into five rhetorical roles: BACKGROUND, OBJECTIVE, METHODS, RESULTS, CONCLUSIONS.

### Final Results

| Test Set | Domain | F1 Macro | Accuracy |
|---|---|---|---|
| PubMed-RCT | Biomedical | 0.83 | 0.88 |
| CSAbstruct | Computer Science | 0.76 | 0.75 |

Cross-domain F1 improved from 0.39 (PubMed-only training) to 0.76 (after CS fine-tuning) — nearly doubling out-of-domain performance.

### Model Deployment

Deployed to Hugging Face Hub: [Himel000/reviewmate-classifier-v1](https://huggingface.co/Himel000/reviewmate-classifier-v1)

### Detailed Evaluation

Full methodology, hyperparameters, and per-class performance documented in [phase-1-evaluation.md](phase-1-evaluation.md).

### Engineering Highlights

- **Two-stage transfer learning** — empirically verified (Stage 2 weights diverge only 0.034 from Stage 1, vs 1.84 from fresh DistilBERT)
- **Scope-aware design** — abstracts-only by deliberate choice; classifier limitations honestly documented
- **Free-tier compute optimization** — max_length 64, FP16, multi-GPU batch sizing within Kaggle T4 x2 constraints
- **Community contribution pipeline** — open issue templates for domain-specific dataset contributions