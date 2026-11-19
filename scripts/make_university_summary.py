#!/usr/bin/env python3
"""Make data/university_summary.json from data/college_town_home_sales.csv.

For each university (the nearest campus, in the `university` column), three figures:

- sales: every row for the university. Each row is one completed sale.
- median_sale_price: the median sale price of sales of $10,000 or more. Sales under
  $10,000 are left out of this figure only (see docs/data_description_sheet.md,
  "Some prices are impossible").
- median_days_on_market: the median of contract_date minus list_date, in days, on
  rows that have BOTH dates. A blank date is never treated as zero, and rows with
  only one date are left out of this figure only. The median is used, not the mean.

Nothing is deduplicated: every row is kept, keyed by listing_id.

Run from anywhere:
    python3 scripts/make_university_summary.py
"""

import csv
import json
import statistics
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

MIN_SALE_PRICE = 10_000
HIGHLIGHT = "University of Illinois Urbana-Champaign"

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "college_town_home_sales.csv"
OUTPUT = ROOT / "data" / "university_summary.json"


def whole_dollars(amount):
    """Round half up to a whole number of dollars. A median of two sales can end in .5."""
    return int(Decimal(str(amount)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def as_number(value):
    """Return a whole number as an int, and a median that ends in .5 as a float."""
    return int(value) if float(value).is_integer() else float(value)


def main():
    universities = {}
    total_rows = 0
    rows_both_dates = 0

    # Read every column as text, so zipcode, county_fips and parcel_number keep their zeros.
    with SOURCE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_rows += 1
            u = universities.setdefault(row["university"], {
                "sales": 0,
                "prices": [],
                "days": [],
                "cities": {},
            })
            u["sales"] += 1
            city = u["cities"].setdefault(row["city"], {"sales": 0, "prices": [], "days": []})
            city["sales"] += 1

            price_text = (row["sale_price"] or "").strip()
            if price_text:
                price = int(price_text)
                if price >= MIN_SALE_PRICE:
                    u["prices"].append(price)
                    city["prices"].append(price)

            list_text = (row["list_date"] or "").strip()
            contract_text = (row["contract_date"] or "").strip()
            if list_text and contract_text:
                days = (date.fromisoformat(contract_text) - date.fromisoformat(list_text)).days
                rows_both_dates += 1
                u["days"].append(days)
                city["days"].append(days)

    def summarise(sales, prices, days):
        return {
            "sales": sales,
            "sales_priced": len(prices),
            "median_sale_price": whole_dollars(statistics.median(prices)) if prices else None,
            "rows_with_both_dates": len(days),
            "median_days_on_market": as_number(statistics.median(days)) if days else None,
        }

    rows = []
    for name, u in universities.items():
        entry = {"university": name}
        entry.update(summarise(u["sales"], u["prices"], u["days"]))
        entry["highlight"] = name == HIGHLIGHT
        entry["cities"] = [
            {"city": city, **summarise(c["sales"], c["prices"], c["days"])}
            for city, c in sorted(u["cities"].items(), key=lambda kv: -kv[1]["sales"])
        ]
        rows.append(entry)
    rows.sort(key=lambda r: r["sales"], reverse=True)

    out = {
        "source": "data/college_town_home_sales.csv",
        "rules": {
            "sales": "Every row for the university.",
            "median_sale_price": f"Median of sales of ${MIN_SALE_PRICE:,} or more. Sales under ${MIN_SALE_PRICE:,} are left out of this figure only.",
            "median_days_on_market": "Median of contract_date minus list_date, in days, on rows with both dates. Blank dates are not treated as zero. Rows with one date are left out of this figure only.",
        },
        "min_sale_price": MIN_SALE_PRICE,
        "highlight": HIGHLIGHT,
        "rows_in_source": total_rows,
        "rows_with_both_dates": rows_both_dates,
        "universities": rows,
    }
    OUTPUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(rows)} universities, "
          f"{rows_both_dates} of {total_rows} rows have both dates")


if __name__ == "__main__":
    main()
