from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pandas as pd

from src.personalize import personalize_company
from src.qualify import qualify_company
from src.research import research_company


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the growth machine on a fresh prospect batch."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="CSV containing company and domain columns.",
    )

    parser.add_argument(
        "--run-id",
        required=True,
        help="Unique name for this run, e.g. run_a.",
    )

    return parser.parse_args()


def ensure_output_directory(run_id: str) -> Path:
    output_dir = Path("outputs") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def flatten_signals(signals: dict) -> str:
    parts = []

    for group, values in signals.items():
        if values:
            parts.append(
                f"{group}: {', '.join(values)}"
            )

    return " | ".join(parts)


def build_campaign_markdown(results: list[dict]) -> str:
    lines = [
        "# Generated Outreach Review",
        "",
        "> Demonstration output only. Nothing in this file was sent.",
        "> Every generated message requires human review.",
        "",
    ]

    for item in results:
        lines.extend(
            [
                f"## {item['company']}",
                "",
                f"**Fit score:** {item['fit_score']}",
                f"**Fit tier:** {item['fit_tier']}",
                f"**Research status:** {item['research_status']}",
                f"**Fetch method:** {item['fetch_method']}",
                "",
                "### Observed public signal",
                "",
                item["observed_signal"],
                "",
                "### Hypothesized document pain",
                "",
                item["pain_hypothesis"],
                "",
                "### Proposed SuperDocs use case",
                "",
                item["use_case_hypothesis"],
                "",
                "### Draft subject",
                "",
                item["subject"],
                "",
                "### Draft email",
                "",
                "```text",
                item["email"],
                "```",
                "",
                "### Draft follow-up",
                "",
                item["follow_up"],
                "",
                "### Evidence",
                "",
                f"Sources: {', '.join(item['source_urls']) or 'No usable source'}",
                "",
                "**SEND STATUS: NOT_SENT**",
                "",
                "---",
                "",
            ]
        )

    return "\n".join(lines)


def build_metrics(results: list[dict], duration_seconds: float) -> dict:
    total = len(results)

    research_success = sum(
        item["research_status"] == "success"
        for item in results
    )

    low_signal = sum(
        item["research_status"] == "low_signal"
        for item in results
    )

    failed = sum(
        item["research_status"] == "failed"
        for item in results
    )

    direct = sum(
        item["fetch_method"] == "direct"
        for item in results
    )

    fallback = sum(
        item["fetch_method"] == "reader_fallback"
        for item in results
    )

    high = sum(
        item["fit_tier"] == "high"
        for item in results
    )

    medium = sum(
        item["fit_tier"] == "medium"
        for item in results
    )

    low = sum(
        item["fit_tier"] == "low"
        for item in results
    )

    unqualified = sum(
        item["fit_tier"] == "unqualified"
        for item in results
    )

    average_fit_score = (
        round(
            sum(item["fit_score"] for item in results) / total,
            1,
        )
        if total
        else 0
    )

    return {
        "prospects_input": total,
        "research_success": research_success,
        "research_low_signal": low_signal,
        "research_failed": failed,
        "direct_fetches": direct,
        "reader_fallbacks": fallback,
        "high_fit": high,
        "medium_fit": medium,
        "low_fit": low,
        "unqualified": unqualified,
        "average_fit_score": average_fit_score,
        "messages_generated": total,
        "messages_sent": 0,
        "human_review_required": total,
        "duration_seconds": round(duration_seconds, 2),
    }


def main():
    args = parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file does not exist: {input_path}"
        )

    df = pd.read_csv(input_path)

    required_columns = {"company", "domain"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Input CSV must contain company and domain columns."
        )

    output_dir = ensure_output_directory(args.run_id)

    start_time = time.time()

    results = []
    raw_research = []

    print("=" * 65)
    print("GROWTH MACHINE")
    print(f"Run: {args.run_id}")
    print(f"Input: {input_path}")
    print(f"Prospects: {len(df)}")
    print("=" * 65)

    for index, row in df.iterrows():
        company = str(row["company"]).strip()
        domain = str(row["domain"]).strip()

        print(
            f"\n[{index + 1}/{len(df)}] Researching {company}..."
        )

        try:
            research = research_company(
                company,
                domain,
            )

            qualification = qualify_company(
                research
            )

            personalization = personalize_company(
                research,
                qualification,
            )

            raw_research.append(research)

            result = {
                "company": company,
                "domain": domain,
                "research_status": research.get(
                    "research_status",
                    "unknown",
                ),
                "fetch_method": research.get(
                    "fetch_method",
                    "unknown",
                ),
                "pages_fetched": research.get(
                    "pages_fetched",
                    0,
                ),
                "total_signals": research.get(
                    "total_signals",
                    0,
                ),
                "signals": flatten_signals(
                    research.get("signals", {})
                ),
                "source_urls": research.get(
                    "source_urls",
                    [],
                ),
                "fit_score": qualification[
                    "fit_score"
                ],
                "fit_tier": qualification[
                    "fit_tier"
                ],
                "fit_reasons": qualification[
                    "fit_reasons"
                ],
                "use_case_hypothesis": personalization[
                    "use_case_hypothesis"
                ],
                "observed_signal": personalization[
                    "observed_signal"
                ],
                "pain_hypothesis": personalization[
                    "pain_hypothesis"
                ],
                "subject": personalization[
                    "subject"
                ],
                "email": personalization[
                    "email"
                ],
                "follow_up": personalization[
                    "follow_up"
                ],
                "human_review_required": True,
                "send_status": "NOT_SENT",
            }

            results.append(result)

            print(
                f"    status={result['research_status']} | "
                f"method={result['fetch_method']} | "
                f"signals={result['total_signals']} | "
                f"fit={result['fit_score']} ({result['fit_tier']})"
            )

        except Exception as exc:
            print(
                f"    ERROR: {type(exc).__name__}: {exc}"
            )

            # One broken prospect must not stop the batch.
            results.append(
                {
                    "company": company,
                    "domain": domain,
                    "research_status": "failed",
                    "fetch_method": "failed",
                    "pages_fetched": 0,
                    "total_signals": 0,
                    "signals": "",
                    "source_urls": [],
                    "fit_score": 0,
                    "fit_tier": "unqualified",
                    "fit_reasons": [
                        f"Pipeline error: {type(exc).__name__}"
                    ],
                    "use_case_hypothesis": (
                        "Insufficient evidence."
                    ),
                    "observed_signal": (
                        "Research did not complete."
                    ),
                    "pain_hypothesis": (
                        "No reliable hypothesis generated."
                    ),
                    "subject": "",
                    "email": "",
                    "follow_up": "",
                    "human_review_required": True,
                    "send_status": "NOT_SENT",
                }
            )

    duration = time.time() - start_time

    metrics = build_metrics(
        results,
        duration,
    )

    # Reviewer-friendly CSV.
    csv_rows = []

    for result in results:
        csv_row = result.copy()

        csv_row["source_urls"] = " | ".join(
            result["source_urls"]
        )

        csv_row["fit_reasons"] = " | ".join(
            result["fit_reasons"]
        )

        csv_rows.append(csv_row)

    pd.DataFrame(csv_rows).to_csv(
        output_dir / "prospects.csv",
        index=False,
    )

    # Complete structured result.
    with open(
        output_dir / "results.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    # Research evidence separately.
    with open(
        output_dir / "research.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            raw_research,
            file,
            indent=2,
            ensure_ascii=False,
        )

    # Human-readable produced piece.
    campaign = build_campaign_markdown(
        results
    )

    with open(
        output_dir / "campaign.md",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(campaign)

    # Measurement for this specific run.
    with open(
        output_dir / "metrics.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metrics,
            file,
            indent=2,
        )

    print("\n" + "=" * 65)
    print("RUN COMPLETE")
    print("=" * 65)

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print(
        f"\nArtifacts saved to: {output_dir.resolve()}"
    )


if __name__ == "__main__":
    main()