# Growth Machine Measurement

## What this experiment measures

This experiment measures whether a small GTM research and personalization machine can:

1. accept a fresh list of target companies;
2. research each company using public company-level information;
3. extract signals relevant to the target audience;
4. qualify the company using deterministic rules;
5. identify specific public evidence for personalization;
6. generate a reviewable outreach hypothesis;
7. distinguish strong evidence from weak evidence;
8. require human review before any possible external use.

This experiment does **not** measure reply rate, conversion rate, meetings booked, or revenue because no outreach was sent.

---

## Final Validation Runs

The final machine was executed twice using the same frozen pipeline.

### Run A

Input:

`inputs/batch_a.csv`

Prospects:

- Persistent Systems
- Coforge
- Hexaware
- Nagarro
- Mphasis

Results:

| Metric | Result |
|---|---:|
| Prospects | 5 |
| Research success | 5 |
| Research failures | 0 |
| Direct fetches | 4 |
| Reader fallbacks | 1 |
| High fit | 2 |
| Medium fit | 3 |
| Average fit score | 59.8 |
| Strong personalization | 2 |
| Usable personalization | 2 |
| Needs review | 1 |
| Average personalization evidence score | 67.0 |
| Draft ready | 2 |
| Draft ready with review | 2 |
| Manual research required | 1 |
| Messages generated | 5 |
| Messages sent | 0 |
| Human review required | 5 |
| Runtime | 38.44 seconds |

---

## Run B

Input:

`inputs/batch_b.csv`

This was a fresh batch processed through the same machine without changing the pipeline between the two final runs.

Prospects:

- Birlasoft
- Happiest Minds
- Sonata Software
- Zensar
- LTIMindtree

Results:

| Metric | Result |
|---|---:|
| Prospects | 5 |
| Research success | 5 |
| Research failures | 0 |
| Direct fetches | 4 |
| Reader fallbacks | 1 |
| High fit | 3 |
| Medium fit | 2 |
| Average fit score | 67.0 |
| Strong personalization | 3 |
| Usable personalization | 1 |
| Needs review | 1 |
| Average personalization evidence score | 72.0 |
| Draft ready | 3 |
| Draft ready with review | 1 |
| Manual research required | 1 |
| Messages generated | 5 |
| Messages sent | 0 |
| Human review required | 5 |
| Runtime | 26.01 seconds |

---

# Combined Funnel

| Stage | Entered | Completed / Routed | Lost |
|---|---:|---:|---:|
| Prospect inputs | 10 | 10 | 0 |
| Public-company research | 10 | 10 | 0 |
| Qualification | 10 | 10 medium/high fit | 0 |
| Evidence-backed personalization | 10 | 8 usable or strong | 2 routed to manual research |
| Strong personalization | 10 | 5 | — |
| Usable with review | 10 | 3 | — |
| Manual research required | 10 | 2 | — |
| Drafts generated | 10 | 10 | 0 |
| Messages sent | 10 drafts | 0 | Not applicable by design |
| Human review required | 10 | 10 | 0 |

---

# Combined Results

Across both final runs:

- 10 prospects were processed.
- 10/10 completed research successfully.
- 0 research jobs failed.
- 8/10 companies were researched directly.
- 2/10 required reader fallback.
- 5 companies were classified as high fit.
- 5 companies were classified as medium fit.
- Average fit score was 63.4.
- 5 personalizations were classified as strong.
- 3 were classified as usable.
- 2 were classified as needs-review.
- Average internal personalization evidence-quality score was 69.5.
- 5 drafts were marked `DRAFT_READY`.
- 3 were marked `DRAFT_READY_WITH_REVIEW`.
- 2 were marked `MANUAL_RESEARCH_REQUIRED`.
- 10 drafts were generated.
- 0 messages were sent.
- All 10 outputs require human review.
- Total runtime across both runs was 64.45 seconds.

The personalization score is an internal evidence-quality heuristic. It is not a prediction of reply rate, buying intent, or outreach success.

---

# Where the Funnel Leaks

## 1. Website accessibility

The clearest technical leak is website accessibility.

Eight prospects could be researched directly, while two required the reader fallback path.

Those same two fallback cases were classified as:

`MANUAL_RESEARCH_REQUIRED`

This is intentional.

A successful website fetch does not automatically mean that the system has sufficiently specific evidence to create a high-confidence personalized message.

---

## 2. Evidence specificity

The machine performs best when it can identify pages such as:

- case studies;
- service pages;
- solution pages;
- industry pages.

These allow personalization to cite concrete public material instead of relying only on generic company positioning.

When page-level evidence is weak, the system lowers the personalization-quality rating rather than pretending the output is equally reliable.

---

## 3. Personalization quality

The current system uses deterministic evidence selection and rule-based personalization.

This makes the system:

- reproducible;
- explainable;
- cheap to run;
- easy to inspect.

However, it can still produce phrasing that requires human editing.

For that reason, even `DRAFT_READY` output is not treated as automatically publishable.

---

# Human-in-the-Loop Boundary

The human reviewer remains responsible for consequential decisions.

Before any draft could be used externally, the reviewer should verify:

1. that the cited source genuinely supports the observed signal;
2. that the evidence is relevant to the prospect;
3. that the pain statement is clearly framed as a hypothesis;
4. that the proposed SuperDocs workflow is supported by product capabilities;
5. that the tone is appropriate;
6. that no unsupported claim about the prospect's internal workflow is made.

The machine never sends outreach.

`send_status` remains:

`NOT_SENT`

for every prospect.

---

# What Breaks at 10x Scale

At 100 or more prospects, the current machine would likely encounter several constraints.

## Rate limiting and anti-bot protection

More websites would block or throttle automated requests.

A larger-scale version would need:

- request throttling;
- caching;
- retry policies;
- domain-specific limits;
- stronger fallback handling.

## Website structure variation

The current research logic uses general heuristics.

At larger scale, websites with unusual navigation, JavaScript-heavy pages, or weak metadata would reduce evidence quality.

## False-positive signals

Keyword-based signal extraction can identify technically correct words that are not actually useful GTM evidence.

At larger scale, this would require stronger semantic classification and evaluation.

## Personalization review workload

Even if research scales automatically, human review becomes the bottleneck.

At 100 prospects, a reviewer should not spend equal time on every account.

The evidence-quality score and draft-status gate are intended to support triage:

- `DRAFT_READY`
- `DRAFT_READY_WITH_REVIEW`
- `MANUAL_RESEARCH_REQUIRED`

## Runtime

The final 10-prospect test took 64.45 seconds across two runs.

A production system would benefit from controlled concurrency, caching, and asynchronous processing rather than simply multiplying the current runtime.

---

# What I Would Measure in a Real Campaign

If external outreach were permitted, I would extend the funnel with:

1. research completion rate;
2. qualification rate;
3. strong-evidence rate;
4. human approval rate;
5. personalization rejection/edit rate;
6. delivery rate;
7. reply rate;
8. positive reply rate;
9. meeting-booked rate;
10. opportunity-created rate;
11. time spent per approved prospect;
12. cost per approved prospect.

Those numbers are deliberately not fabricated here because this experiment sent no outreach.

---

# Current Conclusion

The final test demonstrates that the same machine can process two separate prospect batches end-to-end without changing the pipeline between runs.

The most useful result is not simply that it generated ten drafts.

It also identified where automation should stop.

Eight prospects had sufficient evidence to produce usable or strong personalization, while two were explicitly routed to manual research.

That boundary is important because the goal is not maximum automation at any cost. The goal is repeatable automation with visible evidence, honest uncertainty, and human control.