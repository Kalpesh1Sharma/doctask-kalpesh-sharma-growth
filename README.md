# Growth Machine

This project is my SuperDocs Growth Task submission.

It is a repeatable GTM research and personalization pipeline designed for proposal, bid, and enterprise sales teams at India-headquartered digital engineering and IT-services companies.

The machine takes a simple CSV containing a company name and domain, researches public company-level information, extracts relevant signals, scores the company for fit, forms a document-workflow hypothesis, and generates a personalized campaign draft for human review.

Nothing is automatically sent.

## Target Audience

The audience is deliberately narrow:

**Proposal, bid, and enterprise sales teams at digital engineering and IT-services companies selling complex technology work to enterprise customers.**

These companies often need to adapt existing technical material such as capabilities, delivery approaches, case studies, scope, and industry-specific content for different opportunities.

The machine tests the hypothesis that this repeated proposal-document customization could be a meaningful SuperDocs workflow.

More detail is available in:

`research/audience.md`

## How the Machine Works

The pipeline is:

```text
Company + domain
        ↓
Public website research
        ↓
Signal extraction
        ↓
Fit scoring
        ↓
Document-workflow hypothesis
        ↓
Personalized campaign draft
        ↓
Human review
```

The main modules are:

- `src/research.py` — researches public company websites and extracts company-level signals
- `src/qualify.py` — scores each prospect using deterministic weighted signals
- `src/personalize.py` — creates a company-specific hypothesis and campaign draft
- `main.py` — runs the full pipeline on a batch and saves outputs and metrics

## Resilience

Some enterprise websites block automated requests.

During development, Persistent Systems redirected direct automated traffic to a Radware CAPTCHA.

Instead of creating a company-specific workaround, I added an automatic reader fallback.

The same fallback later handled Zensar during the second batch.

The system therefore follows:

```text
Direct website research
        ↓
Blocked / unusable?
        ↓
Automatic reader fallback
        ↓
Continue pipeline
```

Raw website text is not persisted. The repository stores company-level signals, evidence URLs, and generated outputs.

## Running the Machine

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the first batch:

```bash
python main.py --input inputs/batch_a.csv --run-id run_a
```

Run a fresh second batch:

```bash
python main.py --input inputs/batch_b.csv --run-id run_b
```

The same machine was used for both final runs without modifying the code between them.

## Inputs

### Run A

- Persistent Systems
- Coforge
- Hexaware
- Nagarro
- Mphasis

### Run B

- Birlasoft
- Happiest Minds
- Sonata Software
- Zensar
- LTIMindtree

Each input contains only:

```text
company
domain
```

No named individuals or contact details are stored.

## Final Results

Across the two final runs:

- Prospects processed: 10
- Research success: 10/10
- Research failures: 0
- Direct website fetches: 8
- Automatic reader fallbacks: 2
- High-fit prospects: 5
- Medium-fit prospects: 5
- Average fit score: 62.9
- Campaign drafts generated: 10
- Messages sent: 0
- Human review required: 10/10
- Combined runtime: 53.26 seconds

## Output Structure

Each run creates:

```text
outputs/<run_id>/
├── prospects.csv
├── research.json
├── results.json
├── campaign.md
└── metrics.json
```

### `prospects.csv`

Reviewer-friendly summary containing research status, signals, fit score, and output details.

### `research.json`

Structured research evidence and company-level signals.

### `results.json`

Complete structured result for each prospect.

### `campaign.md`

Human-readable campaign review containing:

- observed public signals
- hypothesized document pain
- proposed SuperDocs use case
- draft subject
- draft email
- draft follow-up
- source evidence
- explicit send status

### `metrics.json`

Run-level reliability and qualification metrics.

## Safety and Restraint

The machine contains no sending capability.

Every generated prospect has:

```text
human_review_required = true
send_status = NOT_SENT
```

The system does not contact companies, scrape personal contact information, or store named individuals.

Public company evidence is used only to generate reviewable hypotheses.

## Known Limitations

### Website accessibility

Some websites use anti-bot systems. The automatic fallback preserves pipeline completion, but fallback research can contain less page-specific detail than direct research.

### Hypothesis vs fact

Public evidence can indicate that a company works in enterprise delivery, engineering, cloud, data, or regulated industries.

It cannot prove the company's internal proposal workflow.

For that reason, generated document pain is explicitly treated as a hypothesis.

### Personalization quality

Direct page access generally produces stronger page-level personalization than fallback research.

### Scaling

At substantially higher volume, the first bottlenecks would likely be:

- anti-bot systems and rate limits
- fallback latency
- inconsistent website structures
- false-positive keyword matching
- human-review capacity

A production version would add caching, rate limiting, stronger semantic classification, and review prioritization.

## Measurement

The complete measurement analysis is available in:

`measurement.md`

It covers:

- what would prove the machine works
- where the funnel leaks
- what breaks first at higher volume
- where humans must remain in the loop
- what downstream metrics I would measure in a permitted real campaign

## Design Decisions

I deliberately chose one channel and made it run end-to-end rather than building several partial channels.

I also intentionally excluded:

- automatic outreach
- personal contact enrichment
- paid enrichment tooling
- multiple acquisition channels
- a complex dashboard
- autonomous sending

The priority was repeatability, evidence, failure recovery, and human review.

## Repository Notes

`PROGRESS.md` records development decisions, observed failures, and final validation.

`TASK.md` records the working scope and assumptions.

This project was built for the SuperDocs Round 2 Growth Task.
