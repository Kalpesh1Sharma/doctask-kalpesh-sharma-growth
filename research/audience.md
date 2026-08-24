# Target Audience and First-Ten Prospect Strategy

## Target Audience

The target audience for this experiment is:

> Bid, proposal, and enterprise-sales teams at India-headquartered digital engineering and IT-services companies selling complex enterprise technology projects to clients in the US, Europe, and other international markets.

This is intentionally narrower than targeting generic sales teams or all software companies.

The machine is designed for companies where selling often involves substantial client-facing documentation such as:

- proposals;
- RFP responses;
- statements of work;
- technical solution documents;
- capability presentations;
- reusable case studies;
- delivery descriptions;
- industry-specific proof points.

The likely internal users are roles such as:

- proposal managers;
- bid managers;
- enterprise sales teams;
- pre-sales teams;
- solution consulting teams;
- sales operations teams.

This experiment targets companies rather than named individuals. No personal contact information was collected.

---

# Why This Audience

Digital engineering and IT-services firms often sell complex, customized engagements rather than a single standardized product.

A single opportunity may require material covering technical capabilities, proposed architecture, delivery approach, industry experience, case studies, compliance considerations, project scope, and implementation methodology.

Much of this material can be reusable across opportunities, but it still needs to be adapted to the specific client. That creates a document-heavy workflow where SuperDocs could plausibly be useful.

---

# Current Workflow Hypothesis

I do not have access to these companies' internal proposal workflows, so the following is deliberately treated as a hypothesis rather than a fact.

A typical proposal workflow may involve:

1. starting from an existing Word document or approved proposal template;
2. copying relevant material from previous proposals;
3. collecting technical input from subject-matter experts;
4. adapting capability descriptions for the current client;
5. replacing case studies and proof points;
6. editing multiple sections manually;
7. checking formatting and document consistency;
8. circulating the document for review;
9. incorporating reviewer changes;
10. producing the final client-facing version.

The likely pain is not simply generating text. The repetitive work is often:

> finding approved material, adapting the right parts, preserving the rest of the document, and keeping the result reviewable.

That is the workflow hypothesis this growth machine is testing.

---

# Why SuperDocs Could Be Relevant

The SuperDocs value proposition I would test for this audience is:

> Start from an existing approved document, update the relevant sections for a new client or opportunity, preserve the surrounding document structure, and keep a human reviewer in control.

The proposed workflow is therefore not:

> "Ask AI to write an entire proposal from scratch."

It is closer to:

> "Use an existing proposal or RFP document, identify the sections that need adaptation, update those sections, and review the changes directly in the document."

This matters because enterprise proposal work often requires both reuse and control.

---

# What Might Make This Audience Switch

The current process is likely acceptable when proposal volume is low or customization is limited.

A team would have a stronger reason to try a different workflow if it could demonstrate:

- less repetitive copy/paste work;
- faster adaptation of approved proposal material;
- preservation of existing document structure;
- easier review of AI-generated changes;
- less switching between chat tools and Word documents;
- more consistent reuse of approved language;
- visible human control before finalization.

The strongest switching trigger would not simply be:

> "AI writes faster."

It would be:

> "We can adapt an existing high-stakes document faster without losing control of the document itself."

---

# Prospect Discovery Method

## How I Would Find the First Ten

The first-ten list was built around companies that publicly demonstrate several characteristics relevant to the hypothesis.

I would search for India-headquartered or India-origin digital engineering and IT-services companies showing evidence of:

1. enterprise technology services;
2. digital engineering or product engineering;
3. cloud, data, AI, or modernization services;
4. work in complex or regulated industries;
5. multiple reusable service, solution, industry, or case-study pages;
6. enterprise engagements that are likely to involve customized technical documentation.

Public discovery sources could include company websites, service pages, industry pages, solution pages, case-study libraries, public company directories, and public search-engine results.

The company domain then becomes the machine's primary research input. The automated pipeline performs deeper public-site research after the initial company is selected.

---

# Selection Criteria

A prospect is more interesting when several of these indicators appear together.

## Enterprise Delivery

Examples of signals:

- enterprise services;
- consulting;
- managed services;
- technology services;
- digital transformation;
- global delivery.

## Engineering Complexity

Examples:

- digital engineering;
- product engineering;
- software engineering;
- platform engineering;
- application development.

## Transformation Work

Examples:

- cloud transformation;
- cloud migration;
- data engineering;
- data modernization;
- analytics;
- AI;
- generative AI.

## Complex Industries

Examples:

- banking;
- financial services;
- insurance;
- healthcare;
- life sciences;
- public sector.

## Proposal Complexity

Signals suggesting potentially document-heavy selling include:

- RFP;
- proposal;
- statement of work;
- client requirements;
- contracts;
- reusable technical capability material.

The machine converts these public signals into a deterministic fit score.

---

# First Ten Prospects

The experiment intentionally uses two batches. This makes it possible to test the machine once and then run the same pipeline again on a fresh input list.

## Batch A

| Company | Domain | Why it fits the test |
|---|---|---|
| Persistent Systems | persistent.com | Public positioning around digital engineering, enterprise technology, banking, and cloud transformation |
| Coforge | coforge.com | Enterprise technology services with specific financial-services and data-related public material |
| Hexaware | hexaware.com | Digital transformation services with detailed public case studies across data, modernization, healthcare, and other enterprise workflows |
| Nagarro | nagarro.com | Technology consulting and digital engineering with enterprise and financial-services positioning |
| Mphasis | mphasis.com | Enterprise technology services with public material around mortgage, insurance, engineering, and other complex client work |

## Batch B

| Company | Domain | Why it fits the test |
|---|---|---|
| Birlasoft | birlasoft.com | Enterprise transformation services with cloud, integration, manufacturing, and modernization offerings |
| Happiest Minds | happiestminds.com | Digital transformation company with public cloud, data-center, ERP, and consulting services |
| Sonata Software | sonata-software.com | Enterprise modernization company with public cloud, data, and generative-AI offerings |
| Zensar | zensar.com | Enterprise technology company with platform engineering, banking, and cloud-transformation positioning |
| LTIMindtree | ltimindtree.com | Large enterprise technology-services company with public industry, transformation, and case-study material |

These companies were used only as public research targets. No employee was targeted. No message was sent.

---

# Why Two Batches

The purpose of separating the prospects into Batch A and Batch B was not simply to produce ten outputs.

The second batch tests whether the machine can operate on fresh inputs without changing the pipeline between runs.

The final workflow was:

```text
Batch A CSV
    ↓
public website research
    ↓
signal extraction
    ↓
fit scoring
    ↓
evidence selection
    ↓
personalization quality assessment
    ↓
draft generation / manual-research routing
```

Then the exact same pipeline was executed on Batch B. No code changes were made between the two final validation runs.

---

# Channel Chosen

The single GTM channel tested is:

> Research-driven outbound email personalization.

The machine produces an outreach draft and follow-up for review. However, the experiment deliberately stops before actual outreach.

Every prospect has:

```text
send_status = NOT_SENT
```

and:

```text
human_review_required = True
```

---

# Human Review Boundary

The machine does not decide that every researched company deserves an outbound message.

Its personalization gate produces one of three statuses:

```text
DRAFT_READY
DRAFT_READY_WITH_REVIEW
MANUAL_RESEARCH_REQUIRED
```

This prevents weak research from being presented with the same confidence as strong company-specific evidence.

In the final ten-prospect experiment:

- 5 were classified `DRAFT_READY`;
- 3 were classified `DRAFT_READY_WITH_REVIEW`;
- 2 were classified `MANUAL_RESEARCH_REQUIRED`.

The final sending decision always remains with a human.

---

# What This Audience Research Does Not Claim

This work does not claim that:

- these companies currently use a specific proposal tool;
- their teams definitely experience the hypothesized pain;
- they are actively evaluating SuperDocs;
- they would buy SuperDocs;
- any named employee should be contacted.

Those questions would require real customer discovery.

This experiment only establishes that the companies publicly exhibit characteristics making them reasonable targets for testing the document-workflow hypothesis.

---

# Research Restraint

Only public company-level information was used.

The experiment intentionally did not collect:

- private company information;
- personal email addresses;
- employee phone numbers;
- named decision-maker details;
- scraped personal profiles.

No outreach was sent to any company or person.
