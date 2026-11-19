#!/usr/bin/env python3
"""Make data/site_summary.json from data/college_town_home_sales.csv.

Headline numbers for the site. The same rule as the city chart applies: sales under
$10,000 are left out of every figure. Prices are whole dollars (halves round up).

- total_sales: sales of $10,000 or more.
- cities: distinct city names among those sales.
- states: distinct state codes among those sales.
- universities: distinct values of the `university` column among those sales.
- median_sale_price: median of sale_price over those sales.

Run from anywhere:
    python3 scripts/make_site_summary.py
"""

import csv
import json
import statistics
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

MIN_SALE_PRICE = 10_000

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "college_town_home_sales.csv"
OUTPUT = ROOT / "data" / "site_summary.json"


def whole_dollars(amount):
    """Round half up to a whole number of dollars. A median of two sales can end in .5."""
    return int(Decimal(str(amount)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def main():
    rows_in_source = 0
    excluded = 0
    prices = []
    cities = set()
    states = set()
    universities = set()

    # Read every column as text, so zipcode, county_fips and parcel_number keep their zeros.
    with SOURCE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows_in_source += 1
            price_text = (row["sale_price"] or "").strip()
            if not price_text or int(price_text) < MIN_SALE_PRICE:
                excluded += 1
                continue
            prices.append(int(price_text))
            cities.add(row["city"])
            states.add(row["state"])
            universities.add(row["university"])

    out = {
        "source": "data/college_town_home_sales.csv",
        "rule": f"Sales under ${MIN_SALE_PRICE:,} are left out of every figure.",
        "min_sale_price": MIN_SALE_PRICE,
        "rows_in_source": rows_in_source,
        "rows_excluded": excluded,
        "total_sales": len(prices),
        "cities": len(cities),
        "states": len(states),
        "universities": len(universities),
        "median_sale_price": whole_dollars(statistics.median(prices)),
    }
    OUTPUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(prices)} sales used, {excluded} excluded")


if __name__ == "__main__":
    main()
