# Growth Machine Measurement



## What would prove this machine works



The machine is designed to move prospects through four measurable stages:



1. Research succeeds.

2. Relevant company-level signals are found.

3. The prospect can be qualified with evidence.

4. A reviewable, company-specific campaign draft is produced.



For this experiment, success means the same pipeline can process two fresh batches without manual repair between runs.



## Experiment results



Ten companies were processed across two independent runs.



- Research success: 10/10

- Research failures: 0

- Direct website fetches: 8

- Automatic fallback fetches: 2

- High-fit prospects: 5

- Medium-fit prospects: 5

- Average fit score: 62.9

- Draft campaign messages generated: 10

- Messages sent: 0

- Human review required: 10/10

- Combined runtime: 53.26 seconds



Run B used fresh inputs and was executed without modifying the machine after the final Run A validation.



## Where the funnel leaks



### Website accessibility



Some company websites reject automated requests.



The system encountered this with Persistent Systems and Zensar and automatically switched to a public-reader fallback.



The fallback preserved pipeline completion, but its research can contain less page-level detail than direct site navigation.



### Signal quality



Keyword evidence can demonstrate that a company works in areas such as enterprise delivery, engineering, cloud, data, or regulated industries.



It cannot prove that the company currently experiences a specific proposal-workflow problem.



For that reason, the output labels document pain as a hypothesis rather than a fact.



### Personalization quality



Directly accessible websites provide stronger page-specific personalization.



Fallback research may produce broader company-level signals and therefore weaker personalization.



## What breaks first at 10x volume



At approximately 100 prospects, the first issues would probably be:



1. website rate limiting and anti-bot systems

2. slower fallback research

3. inconsistent website structures

4. false-positive keyword matching

5. increasing human-review workload



Research should therefore be cached, rate limited, and monitored before scaling.



A production system should also use stronger semantic classification rather than relying only on deterministic keywords.



## Human in the loop



A human remains required before any generated campaign material can be used.



The reviewer should verify:



- source evidence

- whether the inferred pain is reasonable

- whether the use case actually fits the company

- unsupported claims

- tone and personalization



The machine therefore sets `human\_review\_required = true` and `send\_status = NOT\_SENT` for every prospect.



It contains no sending capability.



## What I would measure in a real campaign



Because this assessment prohibits contacting real companies, downstream conversion metrics cannot be measured here.



In a permitted real experiment I would track:



- research completion rate

- qualification rate

- human approval rate

- personalization rejection rate

- outreach delivery rate

- reply rate

- positive reply rate

- meeting conversion

- qualified opportunity conversion

- time and cost per researched prospect



The current experiment measures system reliability and output quality, not real customer conversion.

