from __future__ import annotations


WEIGHTS = {
    "enterprise_delivery": 3,
    "engineering": 2,
    "cloud": 1,
    "data_ai": 1,
    "regulated_industries": 2,
    "proposal_complexity": 4,
}


def _signal_count(signals: dict, group: str) -> int:
    return len(signals.get(group, []))


def _build_fit_reasons(signals: dict) -> list[str]:
    reasons = []

    if _signal_count(signals, "enterprise_delivery"):
        reasons.append(
            "Enterprise delivery signals suggest complex client-facing sales and delivery workflows."
        )

    if _signal_count(signals, "engineering"):
        reasons.append(
            "Engineering services indicate technical scope must often be explained and tailored for clients."
        )

    if _signal_count(signals, "regulated_industries"):
        reasons.append(
            "Work in regulated industries increases the need for careful, reviewable document workflows."
        )

    if _signal_count(signals, "proposal_complexity"):
        reasons.append(
            "Direct proposal/RFP/SOW terminology strongly suggests repeated proposal-document work."
        )

    if _signal_count(signals, "cloud") or _signal_count(signals, "data_ai"):
        reasons.append(
            "Transformation programs typically require customized scopes, timelines, capabilities and case-study material."
        )

    return reasons


def _use_case_hypothesis(signals: dict) -> str:
    engineering = _signal_count(signals, "engineering")
    regulated = _signal_count(signals, "regulated_industries")
    enterprise = _signal_count(signals, "enterprise_delivery")

    if engineering and regulated:
        return (
            "AI-assisted enterprise proposal and RFP customization for technical "
            "projects in regulated industries, with human review before final use."
        )

    if engineering:
        return (
            "AI-assisted proposal and statement-of-work customization for "
            "digital engineering engagements."
        )

    if enterprise:
        return (
            "Reusable enterprise proposal templates that can be adapted to "
            "different client requirements while preserving document structure."
        )

    return (
        "Document workflow automation for repeated client-facing documents, "
        "subject to manual validation of the exact use case."
    )


def qualify_company(research: dict) -> dict:
    signals = research.get("signals", {})

    if research.get("research_status") == "failed":
        return {
            "fit_score": 0,
            "fit_tier": "unqualified",
            "fit_reasons": [
                "Research failed, so the prospect cannot be qualified reliably."
            ],
            "use_case_hypothesis": (
                "Insufficient evidence to form a reliable use-case hypothesis."
            ),
        }

    raw_score = 0

    for group, weight in WEIGHTS.items():
        count = _signal_count(signals, group)

        # Cap each category so repeated keyword occurrence does not
        # disproportionately dominate the score.
        capped_count = min(count, 3)

        raw_score += capped_count * weight

    # Normalize to an interpretable 0-100 score.
    max_score = sum(3 * weight for weight in WEIGHTS.values())

    fit_score = round((raw_score / max_score) * 100)

    if fit_score >= 60:
        fit_tier = "high"
    elif fit_score >= 35:
        fit_tier = "medium"
    else:
        fit_tier = "low"

    reasons = _build_fit_reasons(signals)

    if not reasons:
        reasons = [
            "Only weak public signals were found; manual review is required."
        ]

    return {
        "fit_score": fit_score,
        "fit_tier": fit_tier,
        "fit_reasons": reasons,
        "use_case_hypothesis": _use_case_hypothesis(signals),
    }