#!/usr/bin/env python3
"""Make data/city_median_sale_price.json from data/college_town_home_sales.csv.

For each city, the median sale price of sales of $10,000 or more. Sales under
$10,000 are left out (see docs/data_description_sheet.md, "Some prices are
impossible"). Nothing is deduplicated: every row is kept, keyed by listing_id.

Run from anywhere:
    python3 scripts/make_city_median_prices.py
"""

import csv
import json
import statistics
from pathlib import Path

MIN_SALE_PRICE = 10_000

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "college_town_home_sales.csv"
OUTPUT = ROOT / "data" / "city_median_sale_price.json"


def main():
    prices_by_city = {}
    total_rows = 0
    kept_rows = 0

    # Read every column as text, so zipcode, county_fips and parcel_number keep their zeros.
    with SOURCE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_rows += 1
            price_text = (row["sale_price"] or "").strip()
            if not price_text:
                continue
            price = int(price_text)
            if price < MIN_SALE_PRICE:
                continue
            kept_rows += 1
            prices_by_city.setdefault((row["city"], row["state"]), []).append(price)

    cities = []
    for (city, state), prices in prices_by_city.items():
        cities.append({
            "city": city,
            "state": state,
            "label": f"{city}, {state}",
            "sales": len(prices),
            "median_sale_price": statistics.median(prices),
        })
    cities.sort(key=lambda c: c["median_sale_price"], reverse=True)

    out = {
        "source": "data/college_town_home_sales.csv",
        "rule": f"Sales of ${MIN_SALE_PRICE:,} or more. Sales under ${MIN_SALE_PRICE:,} are left out.",
        "min_sale_price": MIN_SALE_PRICE,
        "rows_in_source": total_rows,
        "rows_used": kept_rows,
        "cities": cities,
    }
    OUTPUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(cities)} cities, {kept_rows} of {total_rows} rows used")


if __name__ == "__main__":
    main()
