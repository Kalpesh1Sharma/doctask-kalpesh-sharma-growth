# TASK

## Objective

Build one small but real growth machine for SuperDocs that can run end-to-end, then run again on a fresh prospect batch without patching the pipeline between runs.

The machine must:

1. target a specific audience;
2. explain what that audience likely does today;
3. explain what could make them switch;
4. explain how the first ten prospects are found;
5. use one repeatable GTM channel;
6. use only public company-level information;
7. never contact a real company or person;
8. produce a real campaign artifact;
9. include an honest measurement page showing funnel leakage, scaling limits, and the human-review boundary.

## Target Audience

Bid, proposal, and enterprise-sales teams at India-headquartered digital engineering and IT-services companies selling complex enterprise technology projects to international clients.

Detailed audience reasoning lives in:

`research/audience.md`

## GTM Channel

The single channel tested is:

> Research-driven outbound email personalization.

The machine generates company-level draft outreach and a follow-up for review.

It does not send anything.

Every prospect is marked:

```text
send_status = NOT_SENT
human_review_required = True
```

## Inputs

The machine accepts a CSV with:

```text
company
domain
```

Final input batches:

```text
inputs/batch_a.csv
inputs/batch_b.csv
```

Batch A and Batch B each contain five companies.

## Pipeline

```text
CSV
↓
public website research
↓
signal extraction
↓
deterministic fit scoring
↓
company-specific evidence selection
↓
personalization evidence-quality scoring
↓
draft-status gate
↓
draft email + follow-up
↓
human review
```

## Research Rules

The research layer:

- uses public company websites only;
- extracts company-level information;
- discovers useful service, solution, industry, and case-study pages;
- avoids named-person enrichment;
- avoids private or personal information;
- records source URLs and page titles;
- detects blocked or low-quality responses;
- uses a reader fallback when direct access fails.

Research output includes:

```text
research_status
fetch_method
pages_fetched
signals
source_urls
page_titles
```

Possible fetch methods:

```text
direct
reader_fallback
failed
```

## Signal Groups

The machine looks for public signals in these groups:

### Enterprise delivery

Examples:

- enterprise;
- digital transformation;
- consulting;
- managed services;
- global delivery;
- technology services.

### Engineering

Examples:

- digital engineering;
- product engineering;
- software engineering;
- application development;
- platform engineering.

### Cloud

Examples:

- cloud transformation;
- cloud migration;
- cloud services;
- cloud modernization;
- cloud native.

### Data and AI

Examples:

- data analytics;
- data engineering;
- artificial intelligence;
- generative AI;
- machine learning;
- data modernization.

### Regulated industries

Examples:

- banking;
- financial services;
- insurance;
- healthcare;
- life sciences;
- public sector.

### Proposal complexity

Examples:

- RFP;
- request for proposal;
- statement of work;
- SOW;
- proposal;
- contract;
- client requirements.

## Qualification Rules

Qualification is deterministic.

Current weights:

```text
enterprise_delivery: 3
engineering: 2
cloud: 1
data_ai: 1
regulated_industries: 2
proposal_complexity: 4
```

Signal counts are capped before normalization.

Final fit score is normalized to 0–100.

Fit tiers:

```text
high: score >= 60
medium: score >= 35
low: score < 35
unqualified: research failure / insufficient evidence
```

The score measures alignment with the experiment's ICP hypothesis.

It does not measure buying intent.

## Personalization Rules

The personalization layer:

- uses actual public page titles where available;
- cleans obvious archive/brand suffixes;
- identifies page type;
- groups evidence by theme;
- prefers coherent evidence;
- avoids combining unrelated evidence;
- falls back to broader company-level signals if specific pages are unavailable;
- frames document pain as a hypothesis rather than a fact.

Possible page types include:

```text
case_study
industry
service
solution
report
other
```

Possible evidence themes include:

```text
financial_services
healthcare
modernization
engineering
manufacturing
general
```

## Personalization Evidence-Quality Score

Each prospect receives an internal evidence-quality score.

The score rewards:

- specific company-page evidence;
- multiple coherent evidence points;
- strong evidence types such as case studies, service pages, solution pages, or industry pages;
- successful direct page-level research.

Possible quality classes:

```text
strong
usable
needs_review
```

Important:

> This score is an internal evidence-quality heuristic only.

It does not predict:

- reply rate;
- conversion;
- buying intent;
- customer interest;
- factual certainty about internal workflow.

## Draft-Status Gate

The machine maps evidence quality to a review status.

```text
strong
→ DRAFT_READY

usable
→ DRAFT_READY_WITH_REVIEW

needs_review
→ MANUAL_RESEARCH_REQUIRED
```

Even `DRAFT_READY` still requires human review.

The system never sends outreach.

## Generated Artifact

Each run produces:

```text
prospects.csv
results.json
research.json
campaign.md
metrics.json
```

### `prospects.csv`

Flattened reviewer-friendly output.

### `results.json`

Full structured result for each prospect.

### `research.json`

Public-site research and source evidence.

### `campaign.md`

Human-readable campaign output containing:

- fit score;
- fit tier;
- research status;
- evidence quality;
- draft status;
- source evidence;
- observed signal;
- pain hypothesis;
- SuperDocs workflow hypothesis;
- subject;
- email draft;
- follow-up;
- `NOT_SENT` status.

### `metrics.json`

Run-level funnel and quality metrics.

## Run Commands

Install:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run Batch A:

```powershell
python main.py --input inputs/batch_a.csv --run-id run_a
```

Run Batch B:

```powershell
python main.py --input inputs/batch_b.csv --run-id run_b
```

The final validation rule is:

> Do not change pipeline code between the final Batch A and Batch B runs.

## Final Validation

### Run A

```text
prospects_input: 5
research_success: 5
research_failed: 0

direct_fetches: 4
reader_fallbacks: 1

high_fit: 2
medium_fit: 3
average_fit_score: 59.8

personalization_strong: 2
personalization_usable: 2
personalization_needs_review: 1
average_personalization_evidence_score: 67.0

draft_ready: 2
draft_ready_with_review: 2
manual_research_required: 1

messages_generated: 5
messages_sent: 0
human_review_required: 5

duration_seconds: 38.44
```

### Run B

```text
prospects_input: 5
research_success: 5
research_failed: 0

direct_fetches: 4
reader_fallbacks: 1

high_fit: 3
medium_fit: 2
average_fit_score: 67.0

personalization_strong: 3
personalization_usable: 1
personalization_needs_review: 1
average_personalization_evidence_score: 72.0

draft_ready: 3
draft_ready_with_review: 1
manual_research_required: 1

messages_generated: 5
messages_sent: 0
human_review_required: 5

duration_seconds: 26.01
```

### Combined

```text
Prospects processed: 10
Research success: 10/10
Research failures: 0

Direct research: 8
Reader fallback: 2

High fit: 5
Medium fit: 5
Average fit score: 63.4

Strong personalization: 5
Usable personalization: 3
Needs review: 2
Average evidence-quality score: 69.5

DRAFT_READY: 5
DRAFT_READY_WITH_REVIEW: 3
MANUAL_RESEARCH_REQUIRED: 2

Drafts generated: 10
Messages sent: 0
Human review required: 10/10

Combined runtime: 64.45 seconds
```

## Success Criteria

The task is considered successful when:

- the audience is specific;
- the first-ten method is documented;
- the machine runs end-to-end;
- a second fresh batch runs without code changes;
- all research uses public company-level information;
- no real person is targeted;
- no real outreach is sent;
- output evidence is inspectable;
- weak evidence is surfaced rather than hidden;
- the campaign artifact is reviewable;
- the measurement page is honest;
- the human-review boundary is explicit.

## Known Limitations

Current limitations include:

- keyword-based signal extraction;
- inconsistent site structures;
- anti-bot protection;
- weaker evidence during fallback research;
- rule-based personalization;
- page-title quality depends on the source website;
- all output still requires human review.

At larger scale I would add:

- caching;
- throttling;
- controlled concurrency;
- retry policies;
- stronger semantic evidence classification;
- evaluation datasets;
- reviewer feedback loops;
- review-priority queues.

## Deliberate Cuts

The project intentionally does not include:

- automatic email sending;
- personal contact scraping;
- named decision-maker enrichment;
- fabricated conversion numbers;
- claims about company internal processes;
- multi-channel outreach;
- unnecessary dashboards.

The goal is a small machine that genuinely runs, remains inspectable, and makes its uncertainty visible.

## Final State

The core machine is frozen.

Final evidence:

```text
outputs/run_a/
outputs/run_b/
```

Supporting documentation:

```text
README.md
TASK.md
PROGRESS.md
measurement.md
research/audience.md
```

No real company or person was contacted.
