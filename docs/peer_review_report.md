# Prompt 16 — Demanding technical peer review

**Reviewed artifact:** `Prompt_15_MANUSCRIPT/main.pdf` (3 pages) and matching `main.tex`, cross-checked against Prompt 13 exploratory `results.csv` and the assignment’s Prompt 16 requirements. **Review type:** critical technical audit, not an independent replication or external peer-review acceptance.

## Overall recommendation: MAJOR REVISION — not submission-ready

The manuscript accurately labels its results exploratory and avoids a fabricated performance gain. However, **unreviewed AI-only correctness judgments prevent confirmatory claims**; two planned research questions lack analyses; the 61/80 held-out selection and 64-token cap need deeper audit; paired comparisons and reproducibility details are incomplete; and the paper is 3 pages versus the assignment’s 6–10-page target. No novelty claim is supported beyond a controlled empirical comparison. Do not submit it as a validated hallucination detector.

## Scope and evidence verified

- The manuscript’s five point estimates match Prompt 13 `results.csv` after rounding: first-1 AUROC 0.506/AP 0.834; first-5 0.397/0.733; first-10 0.380/0.723; full mean 0.470/0.824; max surprise 0.497/0.840.
- Reported common held-out population: 61 with 48 provisionally incorrect, 13 provisionally correct; 48/61 = 78.69% positive prevalence. This is the relevant no-skill AP reference, not evidence of a useful classifier.
- The manuscript openly discloses AI-only annotation, the 64-token cap, and unresolved RQ2/RQ3. No independent annotation review was provided.
- Figures are sourced from Prompt 13 outputs, but this review does not establish independent recalculation of every plotted point.
- The `.bib` metadata have **not** been verified against publisher records. Do not treat citations as verified.

## MAJOR concerns

### M01 — pp. 1–3; Abstract, III-C, V, VII
**Concern:** Unreviewed AI-only labels are treated as targets for all reported metrics; 11 unresolved and other exclusions further narrow the sample.

**Why it matters:** Label errors can change rankings, prevalence and substantive conclusions.

**Concrete remedy:** Obtain blinded independent review with a documented adjudication rubric; rerun metrics on reviewed held-out labels.

### M02 — pp. 2–3; IV-C, V, VII
**Concern:** Only 61/80 held-out examples enter common-population metrics; exclusions combine short responses and unresolved labels, but no attrition breakdown by reason or class is shown.

**Why it matters:** Complete-case selection can bias comparisons and limits external validity.

**Concrete remedy:** Publish a per-reason exclusion flow and compare eligible vs excluded answer lengths and provisional label distribution; include method-specific populations as sensitivity only.

### M03 — pp. 1–3; III-A, VI-B, VI-C
**Concern:** RQ2 and RQ3 are announced but have no executed length-stratified analysis or pilot-frozen confident-error threshold.

**Why it matters:** Two of three research questions are not empirically answered.

**Concrete remedy:** Either execute prespecified RQ2/RQ3 after label review or explicitly narrow title, abstract and research questions to RQ1.

### M04 — pp. 1–2; II, III, V
**Concern:** The paper discusses semantic entropy, SelfCheckGPT and relevance-weighted methods but implements only five likelihood aggregations; no external detector baseline is run.

**Why it matters:** Readers may mistake conceptual comparators for experimental baselines; comparative significance is limited.

**Concrete remedy:** Clearly call them related work only; optionally implement one feasible comparator under identical labels/data and report costs.

### M05 — pp. 2–3; IV-A, IV-B, VII
**Concern:** Exact model/dataset revisions, generation library versions and the final patched runner are not archived/cited within the manuscript.

**Why it matters:** The reported run may not be reproducible under future dependency changes.

**Concrete remedy:** Add revision hashes, dataset checksum, environment lock, exact prompt/chat template, patched source checksum and commands actually executed.

### M06 — pp. 2–3; IV-C, V, VI
**Concern:** 34/100 responses hit the 64-token cap; truncation is acknowledged but no stratified analysis or check for unfinished answers is provided.

**Why it matters:** Truncation may alter factuality labels and full-response scores, confounding comparisons.

**Concrete remedy:** Quantify cap hits within the 61-case analysis; inspect completeness and rerun a predeclared truncation sensitivity analysis without silently changing the frozen primary sample.

### M07 — pp. 1–3; Abstract, V, VI-A
**Concern:** No paired AUROC difference confidence intervals or predefined superiority/noninferiority margin are reported; individual overlapping CIs cannot establish equivalence.

**Why it matters:** The conclusion about comparative performance cannot support equivalence or inferential claims.

**Concrete remedy:** Report paired bootstrap differences (early minus full), CI, class counts, and refrain from claiming equality or noninferiority.

### M08 — pp. 1–3; II, bibliography
**Concern:** Bibliographic metadata are explicitly unverified; the manuscript hardcodes four entries despite a separate .bib file.

**Why it matters:** Citation traceability and literature completeness are inadequate for submission.

**Concrete remedy:** Verify each paper against publisher/arXiv records; correct metadata and use one bibliography source, adding missing closely relevant early-token work only after verification.

### M09 — pp. 1–3; entire paper
**Concern:** Compiled manuscript is three pages against the assignment’s 6–10-page target; limited details on prior work, annotation rubric, and reproducibility.

**Why it matters:** Fails the stated length target and weakens auditability.

**Concrete remedy:** Expand with evidence-backed methodology, audit tables, label protocol, and supplementary robustness checks, not invented findings.

## MINOR concerns

**m01 (p. 1; title, Abstract):** Title suggests factual error detection although all labels are provisional. **Why:** May overstate validation. **Remedy:** Retain “exploratory” prominently in title and first abstract sentence.

**m02 (p. 2; III-B):** Special-token exclusion and whether EOS contributes to full NLL are not operationally specified. **Why:** Small scoring differences can affect reproducibility. **Remedy:** Document token filtering, logit alignment, and exact handling of EOS/padding.

**m03 (p. 2; IV-B):** Smoke-test agreement is described without reporting number of tokens, numerical tolerance or diagnostic method. **Why:** Readers cannot judge scope of scoring verification. **Remedy:** Report two questions × ten tokens, tolerance 0.02, and max discrepancies from the validated Prompt 08 evidence.

**m04 (p. 2; V, figures):** ROC/PR captions omit sample-selection details and exact method eligibility; PDF figure readability should be checked at final print size. **Why:** Plots can be misread outside the text. **Remedy:** Add n=61, 48 positives, exploratory-label warning and no-skill PR baseline in captions; inspect final rendered pages.

**m05 (p. 2; V):** AP is called “AUPRC” without stating it is average precision (stepwise interpolation). **Why:** Different PR integration conventions can yield different numbers. **Remedy:** Specify sklearn average_precision_score (if confirmed in code) and keep AP naming consistent.

**m06 (p. 3; VII):** Author name, affiliation, model revision and versions remain placeholders. **Why:** Not a complete submission artifact. **Remedy:** Replace only with verified details and rerun final compilation.

**m07 (pp. 1–3; language):** “Pilot/calibration” is mentioned although no fitted calibration model or frozen decision threshold is demonstrated. **Why:** Can imply an analysis that did not occur. **Remedy:** Describe the 20-question split as reserved pilot; specify actual operations performed.

## Specific claim checks

- **Novelty:** A new algorithm is **not** shown. The defensible contribution is a controlled exploratory comparison of five likelihood-based statistics on one frozen sample. Do not claim first-ever early-token prediction or a novel detector.
- **Performance:** AUROCs around 0.38–0.51 do not show useful discrimination; high AP must be contextualized by 78.7% provisional error prevalence. Neither an early-token advantage nor equivalence has been established.
- **Data leakage:** No demonstrated leakage was found from the manuscript alone, but no audit of whether labels/thresholds influenced feature selection or manuscript decisions was supplied. Keep held-out labels isolated during threshold design; log all post-hoc analyses.
- **Fairness:** Five scores are evaluated on the same 61 cases, which is a fair within-population comparison, but excludes short answers and is not a comparison to published semantic baselines.
- **Significance:** Overlapping marginal CIs are not a formal paired comparison; avoid saying differences are statistically insignificant without paired intervals or a valid test.
- **Early stopping:** No wall-clock, memory, FLOP or energy savings were measured; do not imply practical efficiency gains.

## Revision gate

**Required before confirmatory claims:** independent label review, adjudication protocol, reproducible paired re-evaluation, and documented selection/truncation sensitivity. **Required before final assignment submission:** accurate bibliography, complete provenance, expansion to the stated manuscript target, verified author information, and PDF visual check.
