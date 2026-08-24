from __future__ import annotations

import re


GENERIC_TITLE_TERMS = {
    "home",
    "homepage",
    "welcome",
    "about us",
}


def _possessive(name: str) -> str:
    return f"{name}'" if name.lower().endswith("s") else f"{name}'s"


def _first_signal(signals: dict, group: str) -> str | None:
    values = signals.get(group, [])
    return values[0] if values else None


def _clean_title(title: str, company: str) -> str:
    """
    Turn a website page title into short reviewer-friendly evidence.

    Example:
    "Product Engineering Services | Digital Innovation – Mphasis"
        -> "Product Engineering Services"
    """

    if not title:
        return ""

    cleaned = re.sub(r"\s+", " ", title).strip()

    # Remove common brand suffixes.
    separators = [" | ", " – ", " — "]

    for separator in separators:
        parts = cleaned.split(separator)

        if len(parts) > 1:
            non_brand_parts = [
                part.strip()
                for part in parts
                if company.lower() not in part.lower()
            ]

            if non_brand_parts:
                cleaned = non_brand_parts[0]
                break

    # Remove trailing "- Company" branding.
    pattern = rf"\s+-\s+{re.escape(company)}.*$"

    cleaned = re.sub(
        pattern,
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).strip()

    # Remove archive/category suffixes, including cases such as:
    # "Cloud Services Archives - Brand"
    cleaned = re.sub(
        r"\s+Archives?\s*(?:[-|–—].*)?$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).strip()

    return cleaned


def _classify_page(url: str, title: str) -> str:
    searchable = f"{url} {title}".lower()

    if "case-study" in searchable or "case study" in searchable:
        return "case_study"

    if "/industries/" in searchable or "/industry/" in searchable:
        return "industry"

    if (
        "/services/" in searchable
        or "/capabilities/" in searchable
        or " services" in searchable
    ):
        return "service"

    if "/solutions/" in searchable or " solution" in searchable:
        return "solution"

    if "/reports/" in searchable or " report" in searchable:
        return "report"

    return "other"


def _evidence_theme(title: str) -> str:
    """
    Classify public evidence into a broad theme so the machine
    does not combine unrelated personalization evidence.
    """

    lower = title.lower()

    if any(
        term in lower
        for term in (
            "banking",
            "financial",
            "insurance",
            "mortgage",
            "capital markets",
        )
    ):
        return "financial_services"

    if any(
        term in lower
        for term in (
            "healthcare",
            "life sciences",
            "clinical",
            "etmf",
            "pharma",
        )
    ):
        return "healthcare"

    if any(
        term in lower
        for term in (
            "cloud",
            "data",
            "analytics",
            "ai",
            "artificial intelligence",
            "modernization",
            "platform",
        )
    ):
        return "modernization"

    if any(
        term in lower
        for term in (
            "engineering",
            "software",
            "product engineering",
            "application development",
        )
    ):
        return "engineering"

    if any(
        term in lower
        for term in (
            "manufacturing",
            "industrial",
            "factory",
            "automation",
        )
    ):
        return "manufacturing"

    return "general"


def _evidence_score(page_type: str, title: str) -> int:
    """
    Score evidence based on specificity and likely GTM usefulness.
    """

    score = {
        "case_study": 6,
        "industry": 5,
        "solution": 5,
        "service": 4,
        "report": 2,
        "other": 1,
    }.get(page_type, 0)

    lower = title.lower()

    useful_terms = (
        "banking",
        "financial",
        "insurance",
        "mortgage",
        "healthcare",
        "life sciences",
        "engineering",
        "cloud",
        "data",
        "analytics",
        "ai",
        "transformation",
        "modernization",
        "automation",
        "platform",
        "enterprise",
    )

    score += sum(
        1
        for term in useful_terms
        if term in lower
    )

    # Extremely long titles often read badly in an outreach hook.
    if len(title.split()) > 14:
        score -= 2

    return score


def _titles_are_too_similar(
    first_title: str,
    second_title: str,
) -> bool:
    """
    Avoid selecting two nearly identical pieces of evidence.
    """

    first_words = set(
        re.findall(
            r"[a-z0-9]+",
            first_title.lower(),
        )
    )

    second_words = set(
        re.findall(
            r"[a-z0-9]+",
            second_title.lower(),
        )
    )

    if not first_words or not second_words:
        return False

    overlap = len(
        first_words & second_words
    ) / max(
        1,
        min(
            len(first_words),
            len(second_words),
        ),
    )

    return overlap >= 0.7


def _specific_public_evidence(
    research: dict,
) -> list[dict]:
    """
    Select strong company-specific public evidence.

    Rules:
    - prefer case studies, industry pages, services, and solutions;
    - use page titles instead of ugly URL-derived fragments;
    - highest-quality evidence becomes the anchor;
    - second evidence point must share the same theme;
    - avoid nearly duplicated evidence.
    """

    company = research["company"]

    urls = research.get(
        "source_urls",
        [],
    )

    titles = research.get(
        "page_titles",
        [],
    )

    evidence = []

    # Index 0 is normally the homepage.
    for index in range(
        1,
        min(
            len(urls),
            len(titles),
        ),
    ):
        url = urls[index]
        raw_title = titles[index]

        title = _clean_title(
            raw_title,
            company,
        )

        if not title:
            continue

        if title.lower() in GENERIC_TITLE_TERMS:
            continue

        page_type = _classify_page(
            url,
            title,
        )

        theme = _evidence_theme(
            title
        )

        evidence.append(
            {
                "title": title,
                "url": url,
                "page_type": page_type,
                "theme": theme,
                "score": _evidence_score(
                    page_type,
                    title,
                ),
            }
        )

    evidence.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    if not evidence:
        return []

    # Strongest item becomes the anchor.
    anchor = evidence[0]

    selected = [anchor]

    # Prefer a coherent second item rather than forcing
    # unrelated evidence into the personalization.
    for item in evidence[1:]:
        if item["theme"] != anchor["theme"]:
            continue

        if _titles_are_too_similar(
            anchor["title"],
            item["title"],
        ):
            continue

        selected.append(item)
        break

    return selected


def _fallback_observed_signal(
    research: dict,
) -> str:
    """
    Used when page-level evidence is unavailable,
    such as during reader fallback.
    """

    signals = research.get(
        "signals",
        {},
    )

    engineering = _first_signal(
        signals,
        "engineering",
    )

    regulated = _first_signal(
        signals,
        "regulated_industries",
    )

    cloud = _first_signal(
        signals,
        "cloud",
    )

    data_ai = _first_signal(
        signals,
        "data_ai",
    )

    enterprise = _first_signal(
        signals,
        "enterprise_delivery",
    )

    parts = []

    if engineering:
        parts.append(engineering)

    if regulated:
        parts.append(regulated)

    if cloud:
        parts.append(cloud)

    if data_ai:
        parts.append(data_ai)

    if enterprise:
        parts.append(enterprise)

    if not parts:
        return (
            "limited public company-level information; "
            "this account needs deeper manual research"
        )

    return (
        "public positioning across "
        + ", ".join(parts[:3])
    )


def _build_observed_signal(
    research: dict,
) -> tuple[str, list[dict]]:
    """
    Produce a natural-language evidence hook.
    """

    evidence = _specific_public_evidence(
        research
    )

    if len(evidence) >= 2:
        first = evidence[0]
        second = evidence[1]

        return (
            f'public material on "{first["title"]}" '
            f'and "{second["title"]}"',
            evidence,
        )

    if len(evidence) == 1:
        item = evidence[0]

        return (
            f'a public page focused on "{item["title"]}"',
            evidence,
        )

    return (
        _fallback_observed_signal(
            research
        ),
        [],
    )


def _engagement_context(
    research: dict,
    evidence: list[dict],
) -> str:
    """
    Turn the selected evidence into a compact context phrase.
    Evidence takes priority over generic keyword signals.
    """

    themes = {
        item.get("theme")
        for item in evidence
    }

    if "financial_services" in themes:
        return (
            "complex financial-services engagements"
        )

    if "healthcare" in themes:
        return (
            "complex healthcare and life-sciences engagements"
        )

    if "modernization" in themes:
        return (
            "cloud, data, and modernization engagements"
        )

    if "engineering" in themes:
        return (
            "technical engineering engagements"
        )

    if "manufacturing" in themes:
        return (
            "complex manufacturing and industrial engagements"
        )

    signals = research.get(
        "signals",
        {},
    )

    if signals.get(
        "regulated_industries"
    ):
        return (
            "complex regulated-industry engagements"
        )

    if signals.get(
        "engineering"
    ):
        return (
            "technical enterprise engagements"
        )

    if (
        signals.get("cloud")
        or signals.get("data_ai")
    ):
        return (
            "technology-transformation engagements"
        )

    return "complex enterprise engagements"


def _build_pain_hypothesis(
    research: dict,
    evidence: list[dict],
) -> str:
    """
    Generate a hypothesis, never claim knowledge of
    the company's internal workflow.
    """

    context = _engagement_context(
        research,
        evidence,
    )

    signals = research.get(
        "signals",
        {},
    )

    has_engineering = bool(
        signals.get("engineering")
    )

    has_regulated = bool(
        signals.get(
            "regulated_industries"
        )
    )

    if (
        has_engineering
        and has_regulated
    ):
        return (
            f"For {context}, proposal teams may need to adapt "
            f"technical scope, proof points, delivery language, "
            f"and reusable case-study material for each opportunity."
        )

    if has_engineering:
        return (
            f"For {context}, proposal teams may repeatedly tailor "
            f"technical scope, delivery approach, and reusable "
            f"capability material."
        )

    return (
        f"For {context}, client-facing teams may repeatedly adapt "
        f"approved material while trying to preserve a consistent "
        f"document structure."
    )


def _personalization_quality(
    research: dict,
    evidence: list[dict],
) -> dict:
    """
    Score personalization quality so a reviewer can see
    when the machine has strong evidence versus a weaker fallback.

    This score measures evidence quality, not company buying intent.
    """

    score = 0
    reasons = []

    if evidence:
        score += 40

        reasons.append(
            "Uses specific company-page evidence."
        )
    else:
        reasons.append(
            "No specific page-level evidence was available."
        )

    if len(evidence) >= 2:
        score += 25

        reasons.append(
            "Uses multiple coherent evidence points."
        )

    if evidence:
        primary_type = evidence[0][
            "page_type"
        ]

        if primary_type == "case_study":
            score += 20

            reasons.append(
                "Primary evidence is a concrete case study."
            )

        elif primary_type in {
            "service",
            "solution",
            "industry",
        }:
            score += 15

            reasons.append(
                "Primary evidence is a specific service, "
                "solution, or industry page."
            )

    if (
        research.get("fetch_method")
        == "direct"
    ):
        score += 15

        reasons.append(
            "Evidence came from direct page-level research."
        )
    else:
        reasons.append(
            "Reader fallback reduced page-level specificity."
        )

    score = min(
        score,
        100,
    )

    if score >= 80:
        quality = "strong"

    elif score >= 55:
        quality = "usable"

    else:
        quality = "needs_review"

    return {
        "personalization_score": score,
        "personalization_quality": quality,
        "personalization_reasons": reasons,
    }


def _build_subject(
    company: str,
    evidence: list[dict],
) -> str:
    if evidence:
        page_type = evidence[0][
            "page_type"
        ]

        if page_type == "case_study":
            return (
                f"A proposal workflow idea for {company}"
            )

        if page_type in {
            "service",
            "solution",
            "industry",
        }:
            return (
                f"Document workflow idea for {company}"
            )

    return (
        f"Proposal workflow idea for {company}"
    )


def _build_email(
    company: str,
    observed_signal: str,
    pain_hypothesis: str,
) -> str:
    return (
        f"Hi {company} team,\n\n"

        f"I was looking through {_possessive(company)} public site "
        f"and noticed {observed_signal}.\n\n"

        f"That made me curious about the document work behind those "
        f"opportunities. {pain_hypothesis}\n\n"

        f"One SuperDocs workflow I would test is starting from an "
        f"approved proposal or RFP document, updating only the "
        f"relevant sections for the opportunity, and leaving the "
        f"result in the document for human review rather than "
        f"producing disconnected copy in a chat window.\n\n"

        f"I would want to validate whether that is actually a painful "
        f"part of your workflow before assuming the fit.\n\n"

        f"Best,\n"
        f"Growth Machine Demo"
    )


def _build_follow_up(
    company: str,
    pain_hypothesis: str,
) -> str:
    return (
        f"Following up on the document-workflow idea for {company}. "

        f"The hypothesis I would want to validate is simple: "
        f"{pain_hypothesis} "

        f"The goal would be to reduce repetitive editing without "
        f"removing proposal-owner review."
    )


def personalize_company(
    research: dict,
    qualification: dict,
) -> dict:
    company = research["company"]

    observed_signal, evidence = _build_observed_signal(
        research
    )

    pain_hypothesis = _build_pain_hypothesis(
        research,
        evidence,
    )

    quality = _personalization_quality(
        research,
        evidence,
    )

    if quality["personalization_quality"] == "strong":
        draft_status = "DRAFT_READY"

    elif quality["personalization_quality"] == "usable":
        draft_status = "DRAFT_READY_WITH_REVIEW"

    else:
        draft_status = "MANUAL_RESEARCH_REQUIRED"

    return {
        "company": company,

        "fit_score": qualification[
            "fit_score"
        ],

        "fit_tier": qualification[
            "fit_tier"
        ],

        "observed_signal": observed_signal,

        "pain_hypothesis": pain_hypothesis,

        "use_case_hypothesis": qualification[
            "use_case_hypothesis"
        ],

        "personalization_evidence": evidence,

        "personalization_score": quality[
            "personalization_score"
        ],

        "personalization_quality": quality[
            "personalization_quality"
        ],

        "personalization_reasons": quality[
            "personalization_reasons"
        ],

        "draft_status": draft_status,

        "subject": _build_subject(
            company,
            evidence,
        ),

        "email": _build_email(
            company,
            observed_signal,
            pain_hypothesis,
        ),

        "follow_up": _build_follow_up(
            company,
            pain_hypothesis,
        ),

        "human_review_required": True,

        "send_status": "NOT_SENT",
    }