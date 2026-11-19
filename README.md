# College-Town Home Sales

## What this site is for

This site shows what homes sold for near 11 US universities. It uses one dataset of 35,442 completed home sales in 18 college towns, collected in March 2026. It answers three questions: how median sale prices compare across the towns, how the median changes with distance from campus, and how the University of Illinois area (Champaign, Urbana and Savoy) compares with the other 10 campus areas. It is for anyone curious about college-town housing, such as buyers, sellers and students of housing markets. It does not give advice about any particular home.

## Live site

https://joshs22.github.io/Website-Project-For-BDI475/

## What is in this repository

| Path | What it is |
|---|---|
| `index.html` | The site: one page, with its charts and tables drawn from the JSON files in `data/` |
| `data/college_town_home_sales.csv` | The dataset, version 1.0: 35,442 rows. The scripts read this file. |
| `data/college_town_home_sales.xlsx`, `.sqlite`, `.duckdb`, `.parquet` | The same data in Excel, SQLite, DuckDB and Parquet formats, with identical values |
| `data/site_summary.json`, `city_median_sale_price.json`, `distance_median_sale_price.json`, `university_summary.json` | The four files the site reads. Scripts make them from the CSV. |
| `docs/data_description_sheet.md` | What every column means, and five problems in the data |
| `scripts/` | The four scripts that make the JSON files |
| `AGENTS.md` | Project instructions for the AI coding agent |
| `AGENT_LOG.md` | The log of work with the AI coding agent |
| `.github/workflows/pages.yml` | Publishes the repository's files to GitHub Pages each time main is pushed. Nothing is built. |

Nothing in the five dataset files has been changed. The site uses only the CSV, through the JSON files made from it.

## Data notes

The figures use the rows as collected. No rows were deduplicated, filled in or corrected. The only cleaning steps are the ones in the data description sheet.

**Rows left out.** The dataset has 35,442 rows. The 40 sales under $10,000 are left out of every median sale price and every distance band. They are still counted in the university table's Sales column, which counts every row (35,442 in total). The summary card counts the 35,402 sales of $10,000 or more.

**Median sale price.** The median of `sale_price` over sales of $10,000 or more, in whole dollars. A median of two sales can end in .5, and those round up. The site shows medians, not averages.

**Median days on market.** `contract_date` minus `list_date`, in days, on the rows that have both dates: 28,042 of 35,442 (79.1%). A blank date is never counted as zero. The median is used, not the mean. This is listing to contract, the way listing sites count it. It is not `sale_date` minus `list_date`, which also includes the time to close.

**Distance bands.** `miles_to_campus` is grouped into under 1 mile, 1 to 3 miles, 3 to 5 miles, 5 to 10 miles, and 10 miles or more. A band includes its lower distance and excludes its upper one, so a home exactly 3.0 miles away is in "3 to 5 miles". Every row has a distance.

**University.** The `university` column, as assigned in the source from each home's coordinates. Champaign, Urbana and Savoy are in the University of Illinois Urbana-Champaign row.

**The five problems in the data description sheet, and how the site handles them:**

1. **Blank dates.** Days on market is computed only where both dates exist, and the page shows how many rows that is. Blanks are not treated as zero.
2. **Repeated addresses.** Nothing is deduplicated. Each row is kept and keyed by `listing_id`, because 66 rows share an address with another row, and many are different apartments in one building.
3. **Impossible prices.** Sales under $10,000 are left out of the median prices and the distance bands. Sales of any price are counted in the Sales column.
4. **`home_type`.** Not used. It is not reliable.
5. **Impossible values, such as zero living area, huge lots, 60 bathrooms, or a $1 billion tax bill.** Not used on the site.

**Differences from the data description sheet.** The sheet's table of 14 college towns takes its medians from sales of $1,000 or more. This site uses $10,000. Thirteen of the 14 medians are the same under either rule. Ann Arbor, MI is $571,000 in the sheet and $572,000 on this site.

**Values as reported.** The values come from one source as collected in March 2026. They were not checked against county records.

## Rerunning the scripts

The site reads four JSON files made from the CSV. To remake them, run these from the repository root. The scripts find the files by their own location, so the folder you run them from does not matter.

```bash
python3 scripts/make_site_summary.py
python3 scripts/make_city_median_prices.py
python3 scripts/make_university_summary.py
python3 scripts/make_distance_median_prices.py
```

- `scripts/make_site_summary.py` writes `data/site_summary.json`: the summary cards at the top of the page.
- `scripts/make_city_median_prices.py` writes `data/city_median_sale_price.json`: the median sale price by city chart.
- `scripts/make_distance_median_prices.py` writes `data/distance_median_sale_price.json`: the median sale price by distance to campus.
- `scripts/make_university_summary.py` writes `data/university_summary.json`: the table of 11 universities and the Champaign, Urbana and Savoy table.

All four use only Python's standard library. Running them again on the same CSV gives the same files, and the dataset files are never changed.

## Tools we used

Claude Code, an AI coding agent. It wrote the scripts and the page under the rules in `AGENTS.md`. The figures were checked against the CSV and the SQLite file, and the page was checked in a headless browser at phone and desktop widths.

Copilot was also used to monitor and fix pull requests if needed.

## Citation

College-town home sales dataset, version 1.0 (2026). University of Illinois-Deloitte Foundation Center for Business Emerging Technologies. Data collected March 2026.

## Who did what

I worked alone. Claude Code wrote the code, and I set the rules in `AGENTS.md`, reviewed each change and checked the figures against the data.
