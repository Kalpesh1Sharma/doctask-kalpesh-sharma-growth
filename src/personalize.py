from __future__ import annotations
from urllib.parse import urlparse

def _possessive(name: str) -> str:
    return f"{name}'" if name.lower().endswith("s") else f"{name}'s"


def _first_signal(signals: dict, group: str) -> str | None:
    values = signals.get(group, [])
    return values[0] if values else None

def _readable_path(url: str) -> str | None:
    path = urlparse(url).path.strip("/")

    if not path:
        return None

    parts = [
        part
        for part in path.split("/")
        if part
        and part.lower()
        not in {
            "home",
            "en",
            "capabilities",
            "services",
            "industries",
            "industry",
            "case-study",
            "case-studies",
        }
    ]

    if not parts:
        return None

    label = parts[-1]

    for suffix in (".html", ".htm", ".aspx", ".php"):
        if label.lower().endswith(suffix):
            label = label[:-len(suffix)]
            break

    return (
        label
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def _specific_public_evidence(research: dict) -> list[str]:
    evidence = []

    for url in research.get("source_urls", [])[1:]:
        label = _readable_path(url)

        if not label:
            continue

        if label not in evidence:
            evidence.append(label)

        if len(evidence) == 2:
            break

    return evidence

def _build_observed_signal(research: dict) -> str:
    signals = research.get("signals", {})
    specific_evidence = _specific_public_evidence(research)

    if specific_evidence:
        if len(specific_evidence) == 1:
            return (
                f"a dedicated public page around "
                f"{specific_evidence[0]}"
            )

        return (
            f"public material around {specific_evidence[0]} "
            f"and {specific_evidence[1]}"
        )

    engineering = _first_signal(signals, "engineering")
    regulated = _first_signal(signals, "regulated_industries")
    enterprise = _first_signal(signals, "enterprise_delivery")

    parts = []

    if engineering:
        parts.append(engineering)

    if regulated:
        parts.append(regulated)

    if enterprise:
        parts.append(enterprise)

    if not parts:
        return (
            "limited public company-level information, "
            "so this hypothesis needs manual validation"
        )

    return "public positioning around " + ", ".join(parts[:3])

def _build_pain_hypothesis(research: dict) -> str:
    signals = research.get("signals", {})

    engineering = bool(signals.get("engineering"))
    regulated = bool(signals.get("regulated_industries"))
    enterprise = bool(signals.get("enterprise_delivery"))

    if engineering and regulated:
        return (
            "Complex technical bids for regulated clients likely require teams "
            "to repeatedly adapt scope, capabilities, case studies and delivery "
            "language while keeping the final document reviewable."
        )

    if engineering and enterprise:
        return (
            "Enterprise engineering proposals likely involve repeated tailoring "
            "of technical scope, delivery approach and reusable capability content."
        )

    if enterprise:
        return (
            "Enterprise sales documents likely require repeated client-specific "
            "editing while preserving a standard proposal structure."
        )

    return (
        "Repeated client-facing documents may create manual editing overhead, "
        "although this should be validated before outreach."
    )


def _build_subject(company: str) -> str:
    return f"Proposal workflow idea for {company}"


def _build_email(
    company: str,
    observed_signal: str,
    pain_hypothesis: str,
) -> str:
    return (
        f"Hi {company} team,\n\n"
        f"I was looking at {_possessive(company)} public site and noticed {observed_signal}.\n\n"
        f"That stood out because teams selling complex enterprise work often "
        f"have to reshape the same technical material for different opportunities. "
        f"My hypothesis is: {pain_hypothesis}\n\n"
        f"SuperDocs is built around editing existing documents rather than "
        f"generating disconnected text in a chat window. A possible workflow "
        f"would be to start from an approved proposal template, adapt selected "
        f"sections for a client or RFP, and keep a human reviewer in control "
        f"before anything is finalized.\n\n"
        f"I'd be curious whether proposal customization is a meaningful document "
        f"workflow for your team.\n\n"
        f"Best,\n"
        f"Growth Machine Demo"
    )


def _build_follow_up(company: str) -> str:
    return (
        f"Following up on the proposal-workflow idea for {company}. "
        f"The use case I had in mind is not replacing proposal owners; "
        f"it is reducing repetitive section-level editing while keeping "
        f"review and approval with the team."
    )


def personalize_company(
    research: dict,
    qualification: dict,
) -> dict:
    company = research["company"]

    observed_signal = _build_observed_signal(research)
    pain_hypothesis = _build_pain_hypothesis(research)

    return {
        "company": company,
        "fit_score": qualification["fit_score"],
        "fit_tier": qualification["fit_tier"],
        "observed_signal": observed_signal,
        "pain_hypothesis": pain_hypothesis,
        "use_case_hypothesis": qualification["use_case_hypothesis"],
        "subject": _build_subject(company),
        "email": _build_email(
            company,
            observed_signal,
            pain_hypothesis,
        ),
        "follow_up": _build_follow_up(company),
        "human_review_required": True,
        "send_status": "NOT_SENT",
    }