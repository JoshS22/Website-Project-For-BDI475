#!/usr/bin/env python3
"""Make data/distance_median_sale_price.json from data/college_town_home_sales.csv.

Sales are grouped by miles_to_campus (straight-line miles to the nearest campus) into
five bands. Each band includes its lower edge and excludes its upper edge, so a home
exactly 1.0 miles away is in "1 to 3 miles", and one exactly 3.0 miles away is in
"3 to 5 miles". For each band:

- sales: the number of sales in the band, of $10,000 or more. Sales under $10,000 are
  left out (see docs/data_description_sheet.md, "Some prices are impossible").
- median_sale_price: the median sale price of those sales, in whole dollars.

Nothing is deduplicated: every row is kept, keyed by listing_id. Distances are read as
exact decimals, so a value of 3.0 lands in the 3 to 5 mile band.

Run from anywhere:
    python3 scripts/make_distance_median_prices.py
"""

import csv
import json
import statistics
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

MIN_SALE_PRICE = 10_000

# (label, lower edge in miles, upper edge in miles or None for no upper edge)
BANDS = [
    ("Under 1 mile", Decimal("0"), Decimal("1")),
    ("1 to 3 miles", Decimal("1"), Decimal("3")),
    ("3 to 5 miles", Decimal("3"), Decimal("5")),
    ("5 to 10 miles", Decimal("5"), Decimal("10")),
    ("10 miles or more", Decimal("10"), None),
]

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "college_town_home_sales.csv"
OUTPUT = ROOT / "data" / "distance_median_sale_price.json"


def whole_dollars(amount):
    """Round half up to a whole number of dollars. A median of two sales can end in .5."""
    return int(Decimal(str(amount)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def band_for(miles):
    """Return the index of the band that holds this distance, or None if it fits no band."""
    for i, (_, low, high) in enumerate(BANDS):
        if miles >= low and (high is None or miles < high):
            return i
    return None


def main():
    prices_by_band = [[] for _ in BANDS]
    total_rows = 0
    rows_unbanded = 0
    rows_under_min = 0

    # Read every column as text, so zipcode, county_fips and parcel_number keep their zeros.
    with SOURCE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_rows += 1

            miles_text = (row["miles_to_campus"] or "").strip()
            if not miles_text:
                rows_unbanded += 1
                continue
            band = band_for(Decimal(miles_text))
            if band is None:
                rows_unbanded += 1
                continue

            price_text = (row["sale_price"] or "").strip()
            if not price_text:
                continue
            price = int(price_text)
            if price < MIN_SALE_PRICE:
                rows_under_min += 1
                continue
            prices_by_band[band].append(price)

    bands_out = []
    for (label, low, high), prices in zip(BANDS, prices_by_band):
        bands_out.append({
            "label": label,
            "from_miles": float(low),
            "to_miles": None if high is None else float(high),
            "sales": len(prices),
            "median_sale_price": whole_dollars(statistics.median(prices)) if prices else None,
        })

    rows_used = sum(len(p) for p in prices_by_band)
    out = {
        "source": "data/college_town_home_sales.csv",
        "rule": (
            f"Sales of ${MIN_SALE_PRICE:,} or more. Sales under ${MIN_SALE_PRICE:,} are left out. "
            "Each band includes its lower distance and excludes its upper one."
        ),
        "min_sale_price": MIN_SALE_PRICE,
        "distance_field": "miles_to_campus",
        "rows_in_source": total_rows,
        "rows_used": rows_used,
        "rows_under_min_price": rows_under_min,
        "rows_without_distance": rows_unbanded,
        "bands": bands_out,
    }
    OUTPUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {rows_used} of {total_rows} rows used")
    for b in bands_out:
        print(f"  {b['label']}: {b['sales']} sales, median {b['median_sale_price']}")


if __name__ == "__main__":
    main()
