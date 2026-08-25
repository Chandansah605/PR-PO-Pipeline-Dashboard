#!/usr/bin/env python3
"""Generate the PR -> PO Journey Board data contract from the committed XLSX files.

The browser consumes journey_board.json.  This module deliberately keeps the
business rules testable and independent from the presentation layer.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path
from statistics import median
from typing import Any, Iterable

import openpyxl


WINDOW_START = date(2026, 4, 1)
EXCLUDED_PR_STATUSES = {"cancelled", "rejected"}
TERMINAL_PO_STATUSES = {"received", "invoiced"}
FM_DEPARTMENTS = {
    "Building Services",
    "Concierge Services",
    "Leisure Services",
    "Security Services",
    "Landscaping Services",
    "Contracted Cleaning Services",
}
HS_DEPARTMENTS = {
    "Home Maintenance Services",
    "Housekeeping Services",
    "Laundry",
}
FITOUT_DEPARTMENTS = {"FitOut Services", "Surveying Services"}
LANE_LABELS = {
    ("Home Services", "CPR"): "HS · CPR",
    ("Factory — Head Office", "PR"): "FACTORY · PR",
    ("Facilities Management", "PR"): "FM · PR",
    ("FitOut Solutions", "CPR"): "FITOUT · CPR",
    ("Facilities Management", "CPR"): "FM · CPR",
    ("FitOut Solutions", "PR"): "FITOUT · PR",
    ("Home Services", "PR"): "HS · PR",
}
BOARD_LANES = {
    ("Home Services", "CPR"),
    ("Factory — Head Office", "PR"),
    ("Facilities Management", "PR"),
    ("FitOut Solutions", "CPR"),
    ("Facilities Management", "CPR"),
}


def text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def parse_datetime(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, time.min)
    raw = text(value).replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw[:19], fmt)
        except ValueError:
            pass
    raise ValueError(f"Unsupported date value: {value!r}")


def working_days(start: Any, end: Any) -> int | None:
    """Equivalent to numpy.busday_count(start, end) with a Mon-Fri calendar."""
    left, right = parse_datetime(start), parse_datetime(end)
    if not left or not right:
        return None
    a, b = left.date(), right.date()
    if b >= a:
        return sum((a + timedelta(days=offset)).weekday() < 5 for offset in range((b - a).days))
    # np.busday_count uses the opposite open/closed boundary when the end is
    # earlier: count weekdays in (end, start], then negate.
    return -sum((b + timedelta(days=offset)).weekday() < 5 for offset in range(1, (a - b).days + 1))


def percentile(values: Iterable[float], fraction: float) -> float | None:
    ordered = sorted(float(v) for v in values)
    if not ordered:
        return None
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * fraction
    low, high = math.floor(position), math.ceil(position)
    if low == high:
        return ordered[low]
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def one_decimal(value: float | int | None) -> float | None:
    return None if value is None else round(float(value), 1)


def division_for(department: Any) -> str:
    department = text(department)
    if department in FM_DEPARTMENTS:
        return "Facilities Management"
    if department in HS_DEPARTMENTS:
        return "Home Services"
    if department in FITOUT_DEPARTMENTS:
        return "FitOut Solutions"
    return "Factory — Head Office"


def requisition_type(number: Any) -> str:
    number = text(number).upper()
    if number.startswith("CPR-"):
        return "CPR"
    if number.startswith("PR-"):
        return "PR"
    return "OTHER"


def is_terminal_po(row: dict[str, Any]) -> bool:
    status = text(row.get("Purchase order status")).lower()
    step = text(row.get("Step name")).lower()
    return status in TERMINAL_PO_STATUSES or "lpo sent" in step or "shared with supplier" in step


def queue_gate(step_name: Any) -> str:
    step = text(step_name).lower()
    if "purchreqreview" in step:
        return "PR Review"
    if "rfq" in step or "inquiry" in step:
        return "RFQ to Suppliers"
    if "quotation received" in step:
        return "Quotation Received"
    if (
        "shared to operations" in step
        or "operations confirms" in step
        or "operations for confirmation" in step
    ):
        return "Ops Confirmation"
    if "unit prices" in step:
        return "Prices Updated"
    return "Mgmt Approvals"


def iso_week_key(value: Any) -> str:
    stamp = parse_datetime(value)
    if not stamp:
        raise ValueError("ISO week requires a timestamp")
    year, week, _ = stamp.isocalendar()
    return f"{year}-W{week:02d}"


def load_xlsx(path: Path) -> list[dict[str, Any]]:
    sheet = openpyxl.load_workbook(path, read_only=True, data_only=True).active
    iterator = sheet.iter_rows(values_only=True)
    headers = [text(value) for value in next(iterator)]
    return [dict(zip(headers, values)) for values in iterator]


def _stats(values: Iterable[float]) -> dict[str, Any]:
    values = [float(value) for value in values]
    return {
        "median": one_decimal(median(values)) if values else None,
        "p90": one_decimal(percentile(values, 0.9)),
        "n": len(values),
    }


def _compact_pr(row: dict[str, Any], age: int | None = None) -> dict[str, Any]:
    result = {
        "number": text(row.get("Purchase requisition")),
        "name": text(row.get("Name")) or "Untitled requisition",
        "department": text(row.get("Department")) or "Factory — Head Office",
        "project": text(row.get("Location")) or "Head Office / not specified",
        "holder": text(row.get("Pending Approver/User")) or "Unassigned",
        "step": text(row.get("Step name")) or "No active workflow step",
        "amount": round(float(row.get("Total amount") or 0), 2),
    }
    if age is not None:
        result["ageWd"] = age
    return result


def _rank_groups(rows: list[dict[str, Any]], field: str, limit: int = 4) -> list[dict[str, Any]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        label = text(row.get(field)) or ("Head Office / not specified" if field == "Location" else "Factory — Head Office")
        grouped[label].append(row["e2eWd"])
    ranked = [
        {"name": name, "medianWd": one_decimal(median(values)), "n": len(values)}
        for name, values in grouped.items()
    ]
    return sorted(ranked, key=lambda item: (-item["medianWd"], -item["n"], item["name"]))[:limit]


def _rank_holders(rows: list[dict[str, Any]], limit: int = 4) -> list[dict[str, Any]]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        grouped[text(row.get("Pending Approver/User")) or "Unassigned"].append(row["ageWd"])
    ranked = [
        {"name": name, "count": len(values), "medianAgeWd": one_decimal(median(values))}
        for name, values in grouped.items()
    ]
    return sorted(ranked, key=lambda item: (-item["count"], -item["medianAgeWd"], item["name"]))[:limit]


def _live_at(
    eligible_prs: list[dict[str, Any]],
    linked_numbers: set[str],
    terminal_by_pr: dict[str, list[datetime]],
    cutoff: datetime,
) -> list[dict[str, Any]]:
    live = []
    for pr in eligible_prs:
        number = text(pr.get("Purchase requisition"))
        created = parse_datetime(pr.get("Created date"))
        if not created or created > cutoff:
            continue
        if text(pr.get("Status")).lower() == "closed" and number not in linked_numbers:
            continue
        if any(stamp <= cutoff for stamp in terminal_by_pr.get(number, [])):
            continue
        item = dict(pr)
        item["ageWd"] = max(0, working_days(created, cutoff) or 0)
        live.append(item)
    return live


def _trend(completed: list[dict[str, Any]], as_of: datetime) -> list[dict[str, Any]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in completed:
        grouped[iso_week_key(row["terminalAt"])].append(row["e2eWd"])
    current_monday = as_of.date() - timedelta(days=as_of.weekday())
    weeks = []
    # Eight full weeks followed by the current partial week.
    for offset in range(8, -1, -1):
        monday = current_monday - timedelta(weeks=offset)
        year, week, _ = monday.isocalendar()
        key = f"{year}-W{week:02d}"
        values = grouped.get(key, [])
        weeks.append(
            {
                "key": key,
                "label": f"W{week:02d}",
                "medianWd": one_decimal(median(values)) if values else None,
                "n": len(values),
                "partial": offset == 0,
            }
        )
    full = [item for item in weeks if not item["partial"] and item["medianWd"] is not None]
    delta = None
    if len(full) >= 2:
        delta = one_decimal(full[-1]["medianWd"] - full[-2]["medianWd"])
    return weeks, delta


def build_board(pr_rows: list[dict[str, Any]], po_rows: list[dict[str, Any]], as_of: datetime | None = None) -> dict[str, Any]:
    source_dates = [
        stamp
        for row in pr_rows + po_rows
        for field in ("Created date", "Created date and time", "Step date and time")
        if (stamp := parse_datetime(row.get(field)))
    ]
    source_as_of = as_of or max(source_dates)
    as_of = datetime.combine(source_as_of.date(), time.min)

    eligible_prs = []
    excluded = Counter()
    pr_by_number = {}
    for row in pr_rows:
        number = text(row.get("Purchase requisition"))
        pr_by_number[number] = row
        created = parse_datetime(row.get("Created date"))
        if not created or created.date() < WINDOW_START:
            excluded["beforeWindow"] += 1
            continue
        if text(row.get("Status")).lower() in EXCLUDED_PR_STATUSES:
            excluded["status"] += 1
            continue
        eligible_prs.append(row)

    eligible_numbers = {text(row.get("Purchase requisition")) for row in eligible_prs}
    linked_numbers = {text(row.get("Purchase requisition")) for row in po_rows if text(row.get("Purchase requisition")) in eligible_numbers}
    terminal_by_pr: dict[str, list[datetime]] = defaultdict(list)
    completed = []
    missing_terminal_timestamp = 0
    terminal_pairs: dict[tuple[str, str], tuple[dict[str, Any], datetime]] = {}
    for po in po_rows:
        number = text(po.get("Purchase requisition"))
        if number not in eligible_numbers or not is_terminal_po(po):
            continue
        terminal_at = parse_datetime(po.get("Step date and time"))
        if not terminal_at:
            missing_terminal_timestamp += 1
            continue
        key = (number, text(po.get("Purchase order")))
        if key not in terminal_pairs or terminal_at < terminal_pairs[key][1]:
            terminal_pairs[key] = (po, terminal_at)

    for po, terminal_at in terminal_pairs.values():
        number = text(po.get("Purchase requisition"))
        terminal_by_pr[number].append(terminal_at)
        pr = pr_by_number[number]
        raised = parse_datetime(pr.get("Created date"))
        submitted = parse_datetime(pr.get("Submitted date"))
        po_created = parse_datetime(po.get("Created date and time"))
        if not all((raised, submitted, po_created, terminal_at)) or not (raised <= submitted <= po_created <= terminal_at):
            excluded["invalidMilestones"] += 1
            continue
        values = {
            "submittedWd": working_days(raised, submitted),
            "poCreatedWd": working_days(raised, po_created),
            "e2eWd": working_days(raised, terminal_at),
            "raisedToSubmittedWd": working_days(raised, submitted),
            "submittedToPoWd": working_days(submitted, po_created),
            "poToLpoWd": working_days(po_created, terminal_at),
        }
        if any(value is None for value in values.values()):
            excluded["invalidMilestones"] += 1
            continue
        terminal_by_pr[number].append(terminal_at)
        item = {**values, **pr}
        item.update(
            {
                "poNumber": text(po.get("Purchase order")),
                "terminalAt": terminal_at,
                "division": division_for(pr.get("Department")),
                "type": requisition_type(number),
            }
        )
        completed.append(item)

    current_live = _live_at(eligible_prs, linked_numbers, terminal_by_pr, as_of)
    yesterday = as_of - timedelta(days=1)
    previous_live = _live_at(eligible_prs, linked_numbers, terminal_by_pr, yesterday)

    e2e = [row["e2eWd"] for row in completed]
    headline = {
        "completed": len(completed),
        "submittedMedianWd": one_decimal(median(row["submittedWd"] for row in completed)) if completed else None,
        "poCreatedMedianWd": one_decimal(median(row["poCreatedWd"] for row in completed)) if completed else None,
        "lpoMedianWd": one_decimal(median(e2e)) if e2e else None,
        "p90Wd": one_decimal(percentile(e2e, 0.9)),
        "within10Pct": one_decimal(sum(value <= 10 for value in e2e) / len(e2e) * 100) if e2e else None,
    }

    def live_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
        ages = [row["ageWd"] for row in rows]
        return {
            "count": len(rows),
            "medianAgeWd": one_decimal(median(ages)) if ages else None,
            "over20": sum(value > 20 for value in ages),
            "within10Pct": one_decimal(sum(value <= 10 for value in ages) / len(ages) * 100) if ages else None,
        }

    live_now, live_previous = live_summary(current_live), live_summary(previous_live)
    live = {
        **live_now,
        "countDelta": live_now["count"] - live_previous["count"],
        "medianAgeDelta": one_decimal((live_now["medianAgeWd"] or 0) - (live_previous["medianAgeWd"] or 0)),
        "over20Delta": live_now["over20"] - live_previous["over20"],
        "within10Delta": one_decimal((live_now["within10Pct"] or 0) - (live_previous["within10Pct"] or 0)),
        "finishedToday": sum(row["terminalAt"].date() == as_of.date() for row in completed),
        "raisedToday": sum(parse_datetime(row.get("Created date")).date() == as_of.date() for row in eligible_prs),
        "oldest": [_compact_pr(row, row["ageWd"]) for row in sorted(current_live, key=lambda item: (-item["ageWd"], text(item.get("Purchase requisition"))))[:10]],
    }

    queues = []
    queue_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pr in eligible_prs:
        if text(pr.get("Status")).lower() != "in review":
            continue
        step_at = parse_datetime(pr.get("Step date and time"))
        if not step_at:
            continue
        row = dict(pr)
        row["dwellDays"] = max(0.0, (as_of - step_at).total_seconds() / 86400)
        queue_rows[queue_gate(pr.get("Step name"))].append(row)
    for gate, rows in queue_rows.items():
        dwells = [row["dwellDays"] for row in rows]
        holders = Counter(text(row.get("Pending Approver/User")) or "Unassigned" for row in rows)
        queues.append(
            {
                "gate": gate,
                "count": len(rows),
                "medianDays": one_decimal(median(dwells)),
                "p90Days": one_decimal(percentile(dwells, 0.9)),
                "holders": [{"name": name, "count": count} for name, count in holders.most_common(4)],
                "oldest": [
                    {**_compact_pr(row), "dwellDays": one_decimal(row["dwellDays"])}
                    for row in sorted(rows, key=lambda item: -item["dwellDays"])[:5]
                ],
            }
        )
    queues.sort(key=lambda item: (-item["count"], -item["medianDays"], item["gate"]))

    completed_by_lane: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    live_by_lane: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in completed:
        completed_by_lane[(row["division"], row["type"])].append(row)
    for row in current_live:
        key = (division_for(row.get("Department")), requisition_type(row.get("Purchase requisition")))
        live_by_lane[key].append(row)

    lanes = []
    for key, rows in completed_by_lane.items():
        if key not in BOARD_LANES:
            continue
        lane_live = live_by_lane.get(key, [])
        cumulative = {
            "submitted": one_decimal(median(row["submittedWd"] for row in rows)),
            "poCreated": one_decimal(median(row["poCreatedWd"] for row in rows)),
            "lpoSent": one_decimal(median(row["e2eWd"] for row in rows)),
        }
        sectors = {
            "raisedToSubmitted": one_decimal(cumulative["submitted"]),
            "submittedToPo": one_decimal(cumulative["poCreated"] - cumulative["submitted"]),
            "poToLpo": one_decimal(cumulative["lpoSent"] - cumulative["poCreated"]),
        }
        lanes.append(
            {
                "id": re.sub(r"[^a-z0-9]+", "-", LANE_LABELS.get(key, " · ".join(key)).lower()).strip("-"),
                "label": LANE_LABELS.get(key, " · ".join(key)),
                "division": key[0],
                "type": key[1],
                "medianWd": cumulative["lpoSent"],
                "p90Wd": one_decimal(percentile((row["e2eWd"] for row in rows), 0.9)),
                "n": len(rows),
                "within10Pct": one_decimal(sum(row["e2eWd"] <= 10 for row in rows) / len(rows) * 100),
                "cumulative": cumulative,
                "sectors": sectors,
                "liveCount": len(lane_live),
                "liveMedianAgeWd": one_decimal(median(row["ageWd"] for row in lane_live)) if lane_live else None,
                "drill": {
                    "projects": _rank_groups(rows, "Location"),
                    "departments": _rank_groups(rows, "Department"),
                    "holders": _rank_holders(lane_live),
                    "oldest": [_compact_pr(row, row["ageWd"]) for row in sorted(lane_live, key=lambda item: -item["ageWd"])[:4]],
                },
            }
        )
    lanes.sort(key=lambda item: (item["medianWd"], -item["n"], item["label"]))
    for position, lane in enumerate(lanes, 1):
        lane["position"] = position

    trend, trend_delta = _trend(completed, as_of)
    projects = _rank_groups(completed, "Location", limit=8)
    slowest_lane = max(lanes, key=lambda item: item["medianWd"])
    slowest_sector = max(
        (
            {"lane": lane["label"], "sector": sector, "medianWd": value}
            for lane in lanes
            for sector, value in lane["sectors"].items()
        ),
        key=lambda item: item["medianWd"],
    )

    def summarise_live(rows: list[dict[str, Any]]) -> dict[str, Any]:
        ages = [row["ageWd"] for row in rows]
        return {
            "count": len(rows),
            "within10Pct": one_decimal(sum(age <= 10 for age in ages) / len(ages) * 100) if ages else None,
            "medianAgeWd": one_decimal(median(ages)) if ages else None,
            "buckets": [
                sum(age <= 5 for age in ages),
                sum(6 <= age <= 10 for age in ages),
                sum(11 <= age <= 20 for age in ages),
                sum(age > 20 for age in ages),
            ],
        }

    def live_delta(now_rows: list[dict[str, Any]], prior_rows: list[dict[str, Any]]) -> dict[str, Any]:
        now, prior = summarise_live(now_rows), summarise_live(prior_rows)
        now["countDelta"] = now["count"] - prior["count"]
        now["within10Delta"] = one_decimal((now["within10Pct"] or 0) - (prior["within10Pct"] or 0))
        now["medianAgeDelta"] = one_decimal((now["medianAgeWd"] or 0) - (prior["medianAgeWd"] or 0))
        return now

    live_types = []
    for req_type in ("CPR", "PR"):
        completed_type = [row for row in completed if row["type"] == req_type]
        live_types.append({
            "type": req_type,
            **live_delta(
                [row for row in current_live if requisition_type(row.get("Purchase requisition")) == req_type],
                [row for row in previous_live if requisition_type(row.get("Purchase requisition")) == req_type],
            ),
            "completed": len(completed_type),
            "completedMedianWd": one_decimal(median(row["e2eWd"] for row in completed_type)) if completed_type else None,
            "toPoMedianWd": one_decimal(median(row["poCreatedWd"] for row in completed_type)) if completed_type else None,
            "afterPoMedianWd": one_decimal(median(row["poToLpoWd"] for row in completed_type)) if completed_type else None,
            "afterPoP90Wd": one_decimal(percentile((row["poToLpoWd"] for row in completed_type), 0.9)) if completed_type else None,
        })

    live_divisions = []
    for division in ("Facilities Management", "Home Services", "FitOut Solutions", "Factory — Head Office"):
        live_divisions.append({
            "division": division,
            **live_delta(
                [row for row in current_live if division_for(row.get("Department")) == division],
                [row for row in previous_live if division_for(row.get("Department")) == division],
            ),
        })

    def typed_queues(req_type: str) -> list[dict[str, Any]]:
        typed: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for gate, rows in queue_rows.items():
            typed[gate].extend(row for row in rows if requisition_type(row.get("Purchase requisition")) == req_type)
        result = []
        for gate, rows in typed.items():
            if not rows:
                continue
            result.append({
                "gate": gate,
                "count": len(rows),
                "medianDays": one_decimal(median(row["dwellDays"] for row in rows)),
            })
        return sorted(result, key=lambda item: (-item["count"], -item["medianDays"], item["gate"]))

    def typed_holders(req_type: str) -> list[dict[str, Any]]:
        grouped: dict[str, list[float]] = defaultdict(list)
        for row in current_live:
            if requisition_type(row.get("Purchase requisition")) != req_type:
                continue
            holder = text(row.get("Pending Approver/User"))
            if not holder:
                continue
            step_at = parse_datetime(row.get("Step date and time"))
            dwell = max(0.0, (as_of - step_at).total_seconds() / 86400) if step_at else 0.0
            grouped[holder].append(dwell)
        result = [
            {"name": holder, "count": len(values), "medianDays": one_decimal(median(values))}
            for holder, values in grouped.items()
        ]
        return sorted(result, key=lambda item: (-item["count"], -item["medianDays"], item["name"]))[:4]

    def typed_oldest(req_type: str) -> list[dict[str, Any]]:
        rows = [row for row in current_live if requisition_type(row.get("Purchase requisition")) == req_type]
        result = []
        for row in sorted(rows, key=lambda item: (-item["ageWd"], text(item.get("Purchase requisition"))))[:3]:
            step_at = parse_datetime(row.get("Step date and time"))
            dwell = max(0.0, (as_of - step_at).total_seconds() / 86400) if step_at else None
            result.append({**_compact_pr(row, row["ageWd"]), "dwellDays": one_decimal(dwell)})
        return result

    yesterday_date = (as_of - timedelta(days=1)).date()
    page_two = {
        "finishedYesterday": sum(row["terminalAt"].date() == yesterday_date for row in completed),
        "raisedYesterday": sum(parse_datetime(row.get("Created date")).date() == yesterday_date for row in eligible_prs),
        "types": live_types,
        "divisions": live_divisions,
        "queues": {req_type: typed_queues(req_type) for req_type in ("CPR", "PR")},
        "holders": {req_type: typed_holders(req_type) for req_type in ("CPR", "PR")},
        "oldest": {req_type: typed_oldest(req_type) for req_type in ("CPR", "PR")},
    }

    return {
        "meta": {
            "schema": 1,
            "windowStart": WINDOW_START.isoformat(),
            "asOf": as_of.date().isoformat(),
            "asOfTimestamp": source_as_of.replace(microsecond=0).isoformat(),
            "generatedAt": source_as_of.replace(microsecond=0).isoformat(),
            "prRows": len(pr_rows),
            "poRows": len(po_rows),
            "eligiblePrs": len(eligible_prs),
            "missingTerminalTimestamp": missing_terminal_timestamp,
            "excluded": dict(excluded),
        },
        "headline": headline,
        "targets": {"raisedToGoodsWd": 10, "goodsToInvoiceDays": 2},
        "trend": trend,
        "trendDeltaWd": trend_delta,
        "live": live,
        "lanes": lanes,
        "queues": queues,
        "pageTwo": page_two,
        "pitWall": {
            "slowestGate": slowest_sector,
            "deepestQueue": queues[0] if queues else None,
            "slowestProject": projects[0] if projects else None,
            "slowestLane": {"label": slowest_lane["label"], "medianWd": slowest_lane["medianWd"]},
            "legacy": {
                "title": "CORRECTIVE — LEGACY DATA",
                "count": 831,
                "text": "831 pre-April CPRs arrived from CRM without department / location (integration gap, fixed ~Apr 2026). Backfill from CRM quotes; until then they are excluded from this board.",
            },
        },
    }


def _json_default(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(f"Cannot serialise {type(value).__name__}")


def sync_embedded_fallback(index_path: Path, pr_rows: list[dict[str, Any]], po_rows: list[dict[str, Any]]) -> None:
    """Make the legacy dashboard fallback literals match the workbook exports."""
    source = index_path.read_text(encoding="utf-8")
    pr_start = source.index("const PR_DATA = ")
    po_start = source.index("const PO_DATA = ", pr_start)
    po_end = source.index("];", po_start) + 2
    pr_json = json.dumps(pr_rows, ensure_ascii=False, separators=(",", ":"), default=_json_default)
    po_json = json.dumps(po_rows, ensure_ascii=False, separators=(",", ":"), default=_json_default)
    replacement = f"const PR_DATA = {pr_json};\nconst PO_DATA = {po_json};"
    index_path.write_text(source[:pr_start] + replacement + source[po_end:], encoding="utf-8", newline="")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", type=Path, default=Path("pr.xlsx"))
    parser.add_argument("--po", type=Path, default=Path("po.xlsx"))
    parser.add_argument("--out", type=Path, default=Path("journey_board.json"))
    parser.add_argument("--as-of", help="Override the source-derived as-of date (YYYY-MM-DD)")
    parser.add_argument("--sync-index", type=Path, help="Also refresh PR_DATA / PO_DATA in index.html")
    args = parser.parse_args()
    pr_rows, po_rows = load_xlsx(args.pr), load_xlsx(args.po)
    as_of = datetime.fromisoformat(args.as_of) if args.as_of else None
    board = build_board(pr_rows, po_rows, as_of)
    args.out.write_text(json.dumps(board, ensure_ascii=False, indent=2, default=_json_default) + "\n", encoding="utf-8")
    if args.sync_index:
        sync_embedded_fallback(args.sync_index, pr_rows, po_rows)
    print(
        f"Wrote {args.out}: {board['headline']['completed']} completed journeys, "
        f"median {board['headline']['lpoMedianWd']} WD, {len(board['lanes'])} lanes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
