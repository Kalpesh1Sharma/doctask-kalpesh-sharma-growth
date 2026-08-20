from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/131 Safari/537.36"
)

TIMEOUT = 12

READER_TIMEOUT = 25

BLOCK_MARKERS = (
    "captcha",
    "access denied",
    "verify you are human",
    "bot detection",
    "radware",
    "cloudflare",
    "security check",
)
MAX_INTERNAL_PAGES = 4

# Pages useful for GTM research.
USEFUL_LINK_TERMS = (
    "services",
    "solutions",
    "industries",
    "industry",
    "capabilities",
    "case-studies",
    "case-study",
    "success-stories",
    "customers",
    "digital-engineering",
    "cloud",
    "data",
    "consulting",
)

# Avoid pages likely to contain named individuals or irrelevant content.
BLOCKED_LINK_TERMS = (
    "leadership",
    "team",
    "people",
    "careers",
    "jobs",
    "investors",
    "press",
    "news",
    "blog",
    "contact",
    "privacy",
    "terms",
)


SIGNAL_GROUPS = {
    "enterprise_delivery": [
        "enterprise",
        "digital transformation",
        "consulting",
        "managed services",
        "global delivery",
        "technology services",
    ],
    "engineering": [
        "digital engineering",
        "product engineering",
        "software engineering",
        "application development",
        "platform engineering",
    ],
    "cloud": [
        "cloud transformation",
        "cloud migration",
        "cloud services",
        "cloud modernization",
        "cloud native",
    ],
    "data_ai": [
        "data analytics",
        "data engineering",
        "artificial intelligence",
        "generative ai",
        "machine learning",
        "data modernization",
    ],
    "regulated_industries": [
        "banking",
        "financial services",
        "insurance",
        "healthcare",
        "life sciences",
        "public sector",
    ],
    "proposal_complexity": [
        "request for proposal",
        "rfp",
        "statement of work",
        "sow",
        "proposal",
        "contract",
        "client requirements",
    ],
}


def _normalize_base_url(domain: str) -> str:
    domain = domain.strip()

    if domain.startswith(("http://", "https://")):
        return domain.rstrip("/")

    return f"https://{domain.rstrip('/')}"


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _same_domain(base_url: str, candidate_url: str) -> bool:
    base_host = urlparse(base_url).netloc.lower().replace("www.", "")
    candidate_host = urlparse(candidate_url).netloc.lower().replace("www.", "")

    return base_host == candidate_host


def _page_text(soup: BeautifulSoup) -> str:
    for element in soup(["script", "style", "noscript", "svg"]):
        element.decompose()

    return _clean_text(soup.get_text(" ", strip=True))


def _fetch(session: requests.Session, url: str) -> dict:
    try:
        response = session.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=True,
        )

        response.raise_for_status()

        content_type = response.headers.get("content-type", "").lower()

        if "text/html" not in content_type:
            return {
                "ok": False,
                "url": url,
                "error": f"Unsupported content type: {content_type}",
            }

        soup = BeautifulSoup(response.text, "html.parser")

        title = ""
        if soup.title and soup.title.string:
            title = _clean_text(soup.title.string)

        meta_description = ""
        description_tag = soup.find(
            "meta",
            attrs={"name": re.compile("^description$", re.I)},
        )

        if description_tag:
            meta_description = _clean_text(
                description_tag.get("content", "")
            )

        return {
            "ok": True,
            "url": response.url,
            "title": title,
            "meta_description": meta_description,
            "text": _page_text(soup),
            "soup": soup,
        }

    except requests.RequestException as exc:
        return {
            "ok": False,
            "url": url,
            "error": str(exc),
        }


def _discover_useful_links(
    base_url: str,
    soup: BeautifulSoup,
) -> list[str]:
    scored_links: list[tuple[int, str]] = []
    seen = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()

        if not href:
            continue

        absolute_url = urljoin(base_url, href)
        parsed = urlparse(absolute_url)

        if parsed.scheme not in ("http", "https"):
            continue

        if not _same_domain(base_url, absolute_url):
            continue

        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")

        if clean_url in seen:
            continue

        seen.add(clean_url)

        searchable = (
            anchor.get_text(" ", strip=True)
            + " "
            + parsed.path.replace("-", " ")
        ).lower()

        if any(term in searchable for term in BLOCKED_LINK_TERMS):
            continue

        score = sum(
            1
            for term in USEFUL_LINK_TERMS
            if term.replace("-", " ") in searchable.replace("-", " ")
        )

        if score:
            scored_links.append((score, clean_url))

    scored_links.sort(key=lambda item: (-item[0], item[1]))

    return [
        url
        for _, url in scored_links[:MAX_INTERNAL_PAGES]
    ]


def _extract_signals(combined_text: str) -> dict[str, list[str]]:
    lower_text = combined_text.lower()
    output = {}

    for group, keywords in SIGNAL_GROUPS.items():
        matched = []

        for keyword in keywords:
            if keyword.lower() in lower_text:
                matched.append(keyword)

        output[group] = matched

    return output

def _looks_blocked(page: dict) -> bool:
    if not page.get("ok"):
        return True

    searchable = (
        page.get("title", "")
        + " "
        + page.get("text", "")[:3000]
        + " "
        + page.get("url", "")
    ).lower()

    return any(marker in searchable for marker in BLOCK_MARKERS)


def _fetch_with_reader(
    session: requests.Session,
    target_url: str,
) -> dict:
    """
    Fallback for public pages that reject direct automated requests.

    Uses Jina Reader to turn a public URL into plain text.
    """
    reader_url = f"https://r.jina.ai/{target_url}"

    try:
        response = session.get(
            reader_url,
            timeout=READER_TIMEOUT,
        )

        response.raise_for_status()

        text = _clean_text(response.text)

        if not text:
            return {
                "ok": False,
                "url": target_url,
                "error": "Reader returned empty content",
            }

        return {
            "ok": True,
            "url": target_url,
            "title": "",
            "meta_description": "",
            "text": text,
            "fetch_method": "reader_fallback",
        }

    except requests.RequestException as exc:
        return {
            "ok": False,
            "url": target_url,
            "error": str(exc),
        }

def research_company(company: str, domain: str) -> dict:
    """
    Research one company using public company-level information only.

    Strategy:
    1. Try direct public website access.
    2. Detect anti-bot / CAPTCHA pages.
    3. Automatically fall back to a public URL reader.
    4. Store signals and sources, not raw website content.
    """

    base_url = _normalize_base_url(domain)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        }
    )

    homepage = _fetch(session, base_url)

    fetch_method = "direct"
    pages = []

    # Direct request failed or landed on CAPTCHA / anti-bot page.
    if _looks_blocked(homepage):
        fallback = _fetch_with_reader(
            session,
            base_url,
        )

        if not fallback["ok"]:
            return {
                "company": company,
                "domain": domain,
                "research_status": "failed",
                "fetch_method": "failed",
                "error": fallback.get(
                    "error",
                    homepage.get("error"),
                ),
                "pages_fetched": 0,
                "source_urls": [],
                "page_titles": [],
                "signals": {},
                "total_signals": 0,
            }

        pages = [fallback]
        fetch_method = "reader_fallback"

    else:
        pages = [homepage]

        useful_links = _discover_useful_links(
            homepage["url"],
            homepage["soup"],
        )

        for url in useful_links:
            page = _fetch(session, url)

            if page["ok"] and not _looks_blocked(page):
                pages.append(page)

    combined_text = " ".join(
        page.get("text", "")
        for page in pages
    )

    signals = _extract_signals(combined_text)

    source_urls = [
        page["url"]
        for page in pages
        if page.get("url")
    ]

    page_titles = [
        page["title"]
        for page in pages
        if page.get("title")
    ]

    total_signals = sum(
        len(values)
        for values in signals.values()
    )

    if total_signals == 0:
        status = "low_signal"
    else:
        status = "success"

    return {
        "company": company,
        "domain": domain,
        "research_status": status,
        "fetch_method": fetch_method,
        "pages_fetched": len(pages),
        "source_urls": source_urls,
        "page_titles": page_titles,
        "signals": signals,
        "total_signals": total_signals,
    }