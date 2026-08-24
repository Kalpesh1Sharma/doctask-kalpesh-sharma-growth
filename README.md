# SuperDocs Growth Machine

A small, repeatable GTM research and personalization machine built for the SuperDocs Round 2 Growth task.

The project tests one narrow hypothesis:

> Bid, proposal, and enterprise-sales teams at India-headquartered digital engineering and IT-services companies may benefit from adapting approved proposal/RFP documents with AI while keeping the existing document structure and a human reviewer in control.

The machine accepts a CSV of company names and domains, researches each company using public company-level information, scores fit, selects evidence for personalization, generates a reviewable draft, and explicitly routes weak-evidence cases to manual research.

No outreach is sent.

---

## What the Machine Does

```text
CSV prospect list
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
reviewable email + follow-up
    ↓
human review
```

The same pipeline was run on two separate prospect batches without changing the code between the final validation runs.

---

## Target Audience

The target audience is:

> Bid, proposal, and enterprise-sales teams at India-headquartered digital engineering and IT-services companies selling complex enterprise technology projects to clients in the US, Europe, and other international markets.

See `research/audience.md` for the full audience rationale, current-workflow hypothesis, switching hypothesis, prospect discovery method, and first-ten strategy.

---

## Repository Structure

```text
.
├── main.py
├── README.md
├── TASK.md
├── PROGRESS.md
├── measurement.md
├── requirements.txt
├── inputs/
│   ├── batch_a.csv
│   └── batch_b.csv
├── outputs/
│   ├── run_a/
│   │   ├── prospects.csv
│   │   ├── results.json
│   │   ├── research.json
│   │   ├── campaign.md
│   │   └── metrics.json
│   └── run_b/
│       ├── prospects.csv
│       ├── results.json
│       ├── research.json
│       ├── campaign.md
│       └── metrics.json
├── research/
│   └── audience.md
└── src/
    ├── research.py
    ├── qualify.py
    └── personalize.py
```

---

## Core Modules

### `src/research.py`

Researches public company websites and:

- fetches company pages;
- discovers useful internal pages;
- avoids people/team/leadership/contact-style targeting;
- extracts company-level GTM signals;
- records source URLs and page titles;
- detects blocked/low-quality responses;
- falls back to a reader path when direct access fails.

Signal groups include enterprise delivery, engineering, cloud, data/AI, regulated industries, and proposal complexity.

### `src/qualify.py`

Uses deterministic rules to score company fit.

Fit tiers:

```text
high
medium
low
unqualified
```

### `src/personalize.py`

Builds reviewable company-level personalization.

It:

- cleans real page titles;
- classifies page type;
- groups evidence by theme;
- prefers coherent evidence;
- avoids forcing unrelated pages together;
- generates an observed public signal;
- generates a cautious pain hypothesis;
- calculates an internal evidence-quality score;
- assigns a draft-status gate.

The personalization score is an **internal evidence-quality heuristic**. It is not a prediction of reply rate, conversion, buying intent, or accuracy.

---

## Draft-Status Gate

Every researched account receives one of three statuses:

```text
DRAFT_READY
DRAFT_READY_WITH_REVIEW
MANUAL_RESEARCH_REQUIRED
```

`DRAFT_READY` means strong page-level public evidence was available. The draft still requires human review.

`DRAFT_READY_WITH_REVIEW` means the evidence is usable but weaker or less complete.

`MANUAL_RESEARCH_REQUIRED` means the company could be researched and qualified, but the machine did not obtain sufficiently specific page-level evidence for reliable personalization.

---

## Safety and Restraint

This repository deliberately has no outreach-sending capability.

For every prospect:

```text
send_status = NOT_SENT
human_review_required = True
```

The experiment uses public company-level information only. It does not intentionally collect personal email addresses, phone numbers, named employee contact lists, private company information, or scraped personal profiles.

Real companies are used only as public research targets. No message was sent to a real company or person.

---

## Installation

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Run the Machine

### Batch A

```powershell
python main.py --input inputs/batch_a.csv --run-id run_a
```

### Batch B

```powershell
python main.py --input inputs/batch_b.csv --run-id run_b
```

The final validation was performed by running Batch A and then Batch B through the same frozen pipeline without changing the code between runs.

---

## Final Prospect Batches

### Batch A

- Persistent Systems
- Coforge
- Hexaware
- Nagarro
- Mphasis

### Batch B

- Birlasoft
- Happiest Minds
- Sonata Software
- Zensar
- LTIMindtree

---

## Final Validation Results

### Run A

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
| Average evidence-quality score | 67.0 |
| Draft ready | 2 |
| Draft ready with review | 2 |
| Manual research required | 1 |
| Messages generated | 5 |
| Messages sent | 0 |
| Human review required | 5 |
| Runtime | 38.44 sec |

### Run B

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
| Average evidence-quality score | 72.0 |
| Draft ready | 3 |
| Draft ready with review | 1 |
| Manual research required | 1 |
| Messages generated | 5 |
| Messages sent | 0 |
| Human review required | 5 |
| Runtime | 26.01 sec |

### Combined

| Metric | Result |
|---|---:|
| Prospects processed | 10 |
| Research success | 10/10 |
| Research failures | 0 |
| Direct fetches | 8 |
| Reader fallbacks | 2 |
| High fit | 5 |
| Medium fit | 5 |
| Average fit score | 63.4 |
| Strong personalization | 5 |
| Usable personalization | 3 |
| Needs review | 2 |
| Average evidence-quality score | 69.5 |
| Draft ready | 5 |
| Draft ready with review | 3 |
| Manual research required | 2 |
| Drafts generated | 10 |
| Messages sent | 0 |
| Human review required | 10/10 |
| Combined runtime | 64.45 sec |

The most useful result is not simply that ten drafts were generated. The machine also identified where automation should stop: eight prospects had strong or usable evidence, while two prospects were routed to manual research.

---

## Output Artifacts

Each run creates:

- `prospects.csv` — flattened reviewer-friendly results;
- `results.json` — full structured results;
- `research.json` — structured public-site research and sources;
- `campaign.md` — human-readable review document with evidence, hypothesis, draft, and explicit `NOT_SENT` status;
- `metrics.json` — run-level metrics.

---

## Reader Fallback and Manual Research

Some public sites block or degrade direct automated access.

In the final validation:

- 8/10 prospects were researched directly;
- 2/10 required reader fallback.

Those two fallback cases were also routed to:

```text
MANUAL_RESEARCH_REQUIRED
```

This is a deliberate safety behavior rather than a hidden failure.

---

## Measurement

See `measurement.md` for the combined funnel, leakage analysis, 10x scaling risks, human-review boundary, limitations, and the metrics that would be measured in a real campaign.

No reply or conversion metrics are claimed because no outreach was sent.

---

## Current Limitations

Known limitations include:

- keyword-based signal extraction can produce false positives;
- website structures vary significantly;
- anti-bot protection can reduce page-level evidence;
- the fallback path can provide less specific evidence;
- page-title quality depends on the source site;
- personalization remains rule-based;
- all output still requires human review.

At larger scale, I would add caching, throttling, controlled concurrency, retry policies, stronger semantic evidence classification, evaluation datasets, reviewer feedback loops, and human-review prioritization.

---

## Deliberate Design Choices

### No automatic outreach

The task is demonstrated without contacting real companies or people.

### No named-person enrichment

The experiment evaluates the audience and company-level GTM hypothesis without collecting personal contact data.

### No unsupported claims about internal workflows

The pain statement is framed as a hypothesis.

### No attempt to maximize automation rate

Weak-evidence accounts are routed to manual research instead of receiving falsely confident drafts.

### No fabricated conversion metrics

The measurement page reports only what the experiment actually measured.

---

## Conclusion

The final experiment shows that one repeatable machine can process two fresh prospect batches using the same pipeline.

Across ten prospects it:

- completed research for all ten;
- qualified all ten;
- generated ten reviewable drafts;
- produced evidence-quality ratings;
- routed two weak-evidence cases to manual research;
- sent zero messages;
- required human review for every output.

The core principle is:

> Automate the repetitive research and document-workflow hypothesis generation, but make uncertainty visible and keep consequential decisions with a human reviewer.
