\# Phase 1: Rhetorical Sentence Classifier — Evaluation Report



\## Summary



A DistilBERT-based classifier was developed via two-stage transfer learning to categorize sentences from research paper abstracts into five rhetorical roles: BACKGROUND, OBJECTIVE, METHODS, RESULTS, CONCLUSIONS.



\*\*Final deployed model:\*\* \[Himel000/reviewmate-classifier-v1](https://huggingface.co/Himel000/reviewmate-classifier-v1)



\## Headline Results



| Test Set | Domain | F1 Macro | F1 Weighted | Accuracy |

|---|---|---|---|---|

| PubMed-RCT | Biomedical (in-domain after Stage 1) | 0.8294 | 0.8825 | 0.8833 |

| CSAbstruct | Computer Science (target domain) | \*\*0.7556\*\* | 0.7527 | 0.7517 |



\## Methodology



\### Two-Stage Transfer Learning



The classifier was trained in two sequential fine-tuning stages, with empirical verification that Stage 2 weights are built upon Stage 1's representations (L2 distance: 0.034 vs 1.84 from a fresh model).



\*\*Stage 1 — Large-scale rhetorical learning\*\*

\- Base model: `distilbert-base-uncased` (66M parameters, 6 Transformer layers)

\- Training data: PubMed-RCT-200k (\~2.2M labeled sentences from \~200k biomedical RCT abstracts)

\- Hyperparameters: 2 epochs, learning rate 5e-5, effective batch size 128 (2× T4 GPUs), max sequence length 64 tokens, FP16 mixed precision

\- Warmup: 500 steps, weight decay: 0.01

\- Compute: \~4 hours on Kaggle T4 x2

\- Purpose: Acquire robust rhetorical pattern recognition from the largest publicly available labeled dataset



\*\*Stage 2 — Computer science domain adaptation\*\*

\- Initialized from Stage 1 weights (in-memory continuation)

\- Training data: CSAbstruct (\~11,000 labeled sentences from 1,668 CS abstracts)

\- Hyperparameters: 4 epochs, learning rate 2e-5 (low to preserve Stage 1 knowledge), batch size 32, max sequence length 64 tokens, FP16

\- Warmup: 100 steps, evaluation/checkpoint every 200 steps

\- Compute: \~3 minutes on Kaggle T4 x2

\- Purpose: Adapt rhetorical patterns to CS/AI scientific writing style



\### Why Two-Stage?



A single-stage model trained only on CSAbstruct (\~11k sentences) lacks the scale needed for robust rhetorical pattern learning. A single-stage model trained only on PubMed (\~2.2M sentences) showed significant cross-domain degradation when evaluated on CS papers (F1 Macro dropped from 0.83 to 0.39).



The two-stage approach combines the strengths of both: large-scale rhetorical pattern learning from PubMed, then domain-specific writing style adaptation from CSAbstruct.



\### Cross-Domain F1 Improvement



| Stage | F1 Macro on CSAbstruct Test |

|---|---|

| After Stage 1 only (PubMed-trained) | 0.3899 |

| After Stage 2 (this model) | 0.7556 |

| \*\*Absolute improvement\*\* | \*\*+0.3657\*\* |



Cross-domain F1 nearly doubled through Stage 2 fine-tuning, validating the staged transfer learning approach for domain transfer.



\## Per-Class Performance on CSAbstruct



| Class | Precision | Recall | F1 | Support |

|---|---|---|---|---|

| BACKGROUND | TBD | TBD | TBD | 493 |

| OBJECTIVE | TBD | TBD | TBD | 155 |

| METHODS | TBD | TBD | TBD | 421 |

| RESULTS | TBD | TBD | TBD | 219 |

| CONCLUSIONS | TBD | TBD | TBD | 61 |



(Per-class breakdown to be added after Stage 2 detailed evaluation re-run.)



\## Label Scheme Alignment



CSAbstruct uses a slightly different label scheme: `{BACKGROUND, OBJECTIVE, METHOD, RESULT, OTHER}`. For evaluation consistency with our PubMed-RCT-trained model, we apply the following mapping:



\- `METHOD → METHODS` (trivial singular/plural)

\- `RESULT → RESULTS` (trivial singular/plural)

\- `OTHER → CONCLUSIONS` (approximate)



The `OTHER → CONCLUSIONS` mapping is based on the observation that OTHER-labeled sentences in CSAbstruct (3% of dataset) predominantly occur in abstract-final positions and contain conclusion-like content (future work statements, implications, summary statements). This is documented as an evaluation assumption.



\## Scope and Limitations



\- Optimized for empirical scientific writing (introduction → method → result → conclusion structure)

\- Strongest performance: CS, AI/ML, applied STEM, quantitative empirical research

\- Performance may degrade on:

&#x20; - Theoretical mathematics (theorem-proof structure)

&#x20; - Humanities and non-empirical writing

&#x20; - Highly LaTeX/equation-heavy methods sections

\- Single-sentence classification (no surrounding sentence context used)

\- Cross-domain expansion to additional fields is part of the project's open contribution roadmap



\## Reproducibility



\- Training notebook: `notebooks/phase-1-training.ipynb` (to be added)

\- Datasets: 

&#x20; - \[PubMed-RCT-200k](https://github.com/Franck-Dernoncourt/pubmed-rct) (Apache 2.0)

&#x20; - \[CSAbstruct](https://huggingface.co/datasets/allenai/csabstruct) (Apache 2.0)

\- Compute: Kaggle Notebooks free tier (2× T4 GPU)



\## Citations



Dernoncourt, F., \& Lee, J. Y. (2017). PubMed 200k RCT: a Dataset for Sequential Sentence Classification in Medical Abstracts. \*Proceedings of the Eighth International Joint Conference on Natural Language Processing\*.



Cohan, A., Beltagy, I., King, D., Dalvi, B., \& Weld, D. (2019). Pretrained Language Models for Sequential Sentence Classification. \*EMNLP 2019\*.

