## Final Growth Machine Validation

The machine was frozen after Run A and executed again on a fresh batch without code changes.

### Run A
- Prospects: 5
- Research success: 5/5
- Direct fetches: 4
- Reader fallbacks: 1
- High fit: 2
- Medium fit: 3
- Average fit score: 59.8
- Messages generated: 5
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
- Messages generated: 5
- Messages sent: 0
- Human review required: 5/5
- Runtime: 26.66 seconds

### Combined
- Prospects processed: 10
- Research success: 10/10
- Failed research: 0
- Direct fetches: 8
- Automatic reader fallbacks: 2
- High fit: 5
- Medium fit: 5
- Average fit score: 62.9
- Messages generated: 10
- Messages sent: 0
- Human review required: 10/10
- Total runtime: 53.26 seconds

### Observed limitation

Some enterprise websites block automated requests. Persistent Systems and Zensar required the automatic reader fallback. This increases latency and creates less granular personalization than direct access. At higher volume, research availability and fallback latency would be one of the first bottlenecks.

No generated outreach was sent to any company.