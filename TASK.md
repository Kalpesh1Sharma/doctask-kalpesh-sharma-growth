# TASK.md

## Objective

Build one working Growth Machine for the SuperDocs Round 2 Growth Task.

The machine must:

1. target one specific, defensible audience;
2. research public company-level information;
3. identify relevant signals and qualify prospects;
4. generate a real campaign asset;
5. run end-to-end on one batch;
6. run again on a fresh batch without patching the code between runs;
7. preserve evidence and measurement;
8. keep a human in the loop;
9. never contact a real person or company.

## Chosen Audience

Proposal, bid, and enterprise sales teams at India-headquartered digital engineering and IT-services firms selling complex enterprise technology work.

The working hypothesis is that these teams repeatedly adapt existing proposal material such as:

- technical capabilities;
- implementation scope;
- delivery approach;
- case studies;
- timelines;
- industry-specific content.

This makes proposal customization a document-editing workflow rather than a blank-page content-generation problem.

## Channel

**Outbound research and personalization.**

The machine does not send outreach.

It only produces reviewable draft campaign material using public company-level information.

## Inputs

Input format:

```csv
company,domain
```

Two independent batches are used.

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

## Pipeline

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

## Research Rules

- Use public company information only.
- Do not research or store named individuals.
- Do not collect personal contact details.
- Avoid leadership, people, team, careers, and similar pages.
- Do not persist raw website text.
- Persist source URLs and company-level signals only.
- If direct access is blocked or unusable, use the automatic public-reader fallback.

## Qualification Rules

The fit score is deterministic and derived from visible signal categories.

Weighted signal groups include:

- enterprise delivery;
- engineering;
- cloud;
- data / AI;
- regulated industries;
- proposal complexity.

Repeated occurrences are capped so one category cannot dominate the score unfairly.

Fit tiers:

- High: score >= 60
- Medium: score >= 35
- Low: score < 35
- Unqualified: research failure

The score is a prioritization tool, not proof of buying intent.

## Personalization Rules

Generated campaign material must:

- reference public company-level evidence;
- distinguish observed facts from inferred pain;
- present document pain as a hypothesis;
- avoid unsupported claims;
- keep the existing product capabilities within what SuperDocs can actually do;
- require human review before any real-world use.

Every result must contain:

```text
human_review_required = true
send_status = NOT_SENT
```

## Resilience Requirement

The machine must not fail simply because one website blocks automated access.

Observed failure mode:

- Persistent Systems redirected automated traffic to a Radware CAPTCHA.

Implemented response:

- detect anti-bot / unusable response;
- automatically switch to a public-reader fallback;
- continue the same pipeline without company-specific code.

The fallback later handled Zensar during the fresh second batch.

## Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Batch A:

```bash
python main.py --input inputs/batch_a.csv --run-id run_a
```

Run Batch B:

```bash
python main.py --input inputs/batch_b.csv --run-id run_b
```

## Final Validation Rule

After the final Run A validation, the machine is frozen.

Run B must execute on fresh inputs using the same code.

No code changes are allowed between the final Run A and Run B unless Run B completely fails and the limitation is documented.

## Success Criteria

The final machine is considered complete when:

- both batches process end-to-end;
- the second batch runs without code patching;
- outputs are saved for every prospect;
- source evidence is preserved;
- generated campaign drafts are reviewable;
- no outreach is sent;
- human review is required for every prospect;
- metrics are saved for each run;
- limitations and scaling bottlenecks are documented.

## Final Results

### Run A

- Prospects: 5
- Research success: 5/5
- Direct fetches: 4
- Reader fallbacks: 1
- High fit: 2
- Medium fit: 3
- Average fit score: 59.8
- Drafts generated: 5
- Messages sent: 0
- Human review required: 5/5
- Runtime: 26.60 seconds

### Run B

- Prospects: 5
- Research success: 5/5
- Direct fetches: 4
- Reader fallbacks: 1
- High fit: 3
- Medium fit: 2
- Average fit score: 66.0
- Drafts generated: 5
- Messages sent: 0
- Human review required: 5/5
- Runtime: 26.66 seconds

### Combined

- Prospects processed: 10
- Research success: 10/10
- Research failures: 0
- Direct fetches: 8
- Automatic reader fallbacks: 2
- High fit: 5
- Medium fit: 5
- Average fit score: 62.9
- Drafts generated: 10
- Messages sent: 0
- Human review required: 10/10
- Combined runtime: 53.26 seconds

## Known Limitations

1. Public website evidence cannot prove a company's internal proposal workflow.
2. Reader fallback can produce less page-specific evidence than direct navigation.
3. Keyword matching can produce false positives.
4. Website structures vary significantly.
5. Anti-bot systems and rate limits become more important at higher volume.
6. Human-review workload becomes a scaling bottleneck.

## Deliberate Cuts

To prioritize a complete, repeatable machine, the following were intentionally not built:

- automatic sending;
- contact-data enrichment;
- paid enrichment tooling;
- multiple acquisition channels;
- complex dashboarding;
- autonomous outreach;
- unnecessary integrations.

## Human-in-the-Loop Boundary

A human must verify:

- source evidence;
- whether the pain hypothesis is reasonable;
- whether the prospect actually fits the use case;
- unsupported or misleading claims;
- tone and personalization.

The machine is a research and drafting system, not an autonomous sales agent.
