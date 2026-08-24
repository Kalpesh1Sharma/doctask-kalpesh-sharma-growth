# Progress Log

## Goal

Build one repeatable GTM machine for a narrow SuperDocs audience that:

- researches public company information;
- qualifies prospects;
- generates evidence-backed personalization;
- runs on a fresh second batch without patching;
- never contacts real people or companies;
- keeps a human reviewer in control.

---

## 1. Audience Selected

Target audience:

> Bid, proposal, and enterprise-sales teams at India-headquartered digital engineering and IT-services companies selling complex enterprise technology projects.

The working hypothesis is that these teams may repeatedly adapt proposal, RFP, case-study, capability, and technical material while preserving document structure and reviewability.

Detailed reasoning:

`research/audience.md`

---

## 2. Initial Machine

The first version implemented:

```text
CSV
→ public website research
→ signal extraction
→ deterministic fit scoring
→ workflow hypothesis
→ personalized email draft
→ human review
```

The first two batches both ran successfully.

However, review of the generated personalization exposed a quality problem.

Some hooks were based on URL-derived phrases and could sound mechanical rather than carefully researched.

Example of the failure mode:

```text
public material around leader isg provider lens...
```

The pipeline worked technically, but personalization quality was not strong enough.

---

## 3. Research Resilience

Some company websites blocked direct automated access.

Persistent Systems produced an anti-bot response during testing.

A reader fallback path was added so research could continue without manually patching the prospect.

The same fallback behavior later handled Zensar.

The fallback is now visible through:

```text
fetch_method = reader_fallback
```

rather than being hidden.

---

## 4. Personalization Upgrade

The personalization system was redesigned to use actual public page titles rather than URL fragments.

It now:

- cleans public page titles;
- identifies page type;
- groups evidence into themes;
- scores evidence usefulness;
- prefers coherent evidence;
- avoids combining unrelated evidence;
- uses evidence before generic keyword signals.

For example, Hexaware now uses coherent public case-study evidence around:

- data platform modernization;
- managed data delivery and reporting.

This produces a much more specific company-level hook.

---

## 5. Evidence-Quality Scoring

A separate personalization evidence-quality heuristic was added.

Possible classifications:

```text
strong
usable
needs_review
```

The score measures the quality of public evidence available to support personalization.

It does not predict:

- buying intent;
- conversion;
- reply rate;
- customer interest.

Reasons for the quality score are saved with every prospect.

---

## 6. Draft Safety Gate

The machine no longer treats every generated draft as equally ready.

Each prospect receives one of:

```text
DRAFT_READY
DRAFT_READY_WITH_REVIEW
MANUAL_RESEARCH_REQUIRED
```

Weak page-level evidence is therefore visible rather than hidden.

All statuses still require human review before any external use.

No sending capability exists.

---

## 7. Final Run A

Input:

`inputs/batch_a.csv`

Companies:

- Persistent Systems
- Coforge
- Hexaware
- Nagarro
- Mphasis

Results:

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

---

## 8. Final Run B

Input:

`inputs/batch_b.csv`

Companies:

- Birlasoft
- Happiest Minds
- Sonata Software
- Zensar
- LTIMindtree

The same frozen pipeline was used without changing code between the final Run A and Run B.

Results:

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

---

## 9. Combined Final Result

Across both final runs:

```text
Prospects: 10
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

The two prospects that required reader fallback were also routed to manual research.

That behavior is intentional: successful broad research does not automatically imply sufficient evidence for confident personalization.

---

## 10. Current Limitations

Known limitations include:

- keyword-based signal detection;
- inconsistent website structures;
- anti-bot protection;
- weaker evidence through fallback research;
- rule-based personalization;
- page-title quality depends on source websites;
- human review remains necessary.

At larger scale I would add:

- caching;
- rate limiting;
- controlled concurrency;
- semantic evidence classification;
- evaluation datasets;
- reviewer feedback;
- review-priority queues.

---

## Final State

The core machine is now frozen.

Final evidence lives in:

```text
outputs/run_a/
outputs/run_b/
```

Supporting documentation:

```text
README.md
TASK.md
measurement.md
research/audience.md
```

No real outreach was performed.
