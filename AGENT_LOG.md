# Agent log

Add a dated entry each time you work with your AI coding agent, with the newest entry at the bottom. Each entry records what you asked the agent, what it produced, and what you checked or changed. Paste your key prompts in exactly as you typed them. Include at least one time the agent got something wrong, and how you caught it.

Copy this outline for each entry:

```markdown
## YYYY-MM-DD: What you worked on

- **Asked:** "Paste your prompt here."
- **Agent produced:** What it made or changed.
- **Checked or changed:** How you checked it, and what you fixed.
```

## 2026-11-19: Median sale price by city chart

- **Asked:** "[Paste the exact prompt for the city chart here. It was given in an earlier session and is not in this session's record, so it is not reconstructed here.]"
- **Agent produced:** `scripts/make_city_median_prices.py`, which writes `data/city_median_sale_price.json`, and the first bar chart on the page: one bar per city, sorted by median, with a rule line saying sales under $10,000 are left out.
- **Checked or changed:** The first version wrote each median without rounding, so Pittsboro, NC showed **$876,985.5**. A median of two sales can end in .5, and a dollar figure cannot. It was fixed by rounding half up to whole dollars (commit `5851cbc`), so the JSON now shows `876986`. In the final check, all 18 city medians were recomputed from the CSV and from the SQLite file, and they matched.

## 2026-11-19: University of Illinois area section

- **Asked:** "Read AGENTS.md and docs/data_description_sheet.md again. Add a section about the University of Illinois area (Champaign, Urbana, Savoy). Using a script in scripts/ that writes a new JSON file in data/, compute for each university: number of sales, median sale price (sales of $10,000 or more), and median days on market, calculated as contract_date minus list_date only on rows that have both dates. Never treat a blank date as zero, and use the median, not the mean. Show this as a table or bar chart, highlight the University of Illinois row, and add a note saying how many rows had both dates. Tell me how to check it."
- **Agent produced:** `scripts/make_university_summary.py`, which writes `data/university_summary.json`. A table of all 11 universities with the Illinois row highlighted, a note giving the count of rows with both dates, and a table of Champaign, Urbana and Savoy. The page's rule line now says the $10,000 rule applies to median prices, since the sales count includes every sale.
- **Checked or changed:** Ran the script twice and got the same file. The 11 sales counts add up to all 35,442 rows, and the both-dates count (28,042) and same-day count (384) match the data description sheet. The Illinois figures were recomputed from the SQLite file and matched.

## 2026-11-19: Median sale price by distance to campus

- **Asked:** "Add a chart of median sale price by distance to campus, using miles_to_campus in these bands: under 1 mile, 1–3 miles, 3–5 miles, 5–10 miles, and 10+ miles. Use sales of $10,000 or more, show the number of sales in each band, and state the rule on the page. Compute everything in a script in scripts/ that saves a new JSON file in data/. Keep the same page style, and make sure it looks right on a phone."
- **Agent produced:** `scripts/make_distance_median_prices.py`, which writes `data/distance_median_sale_price.json`. A bar chart in the page's existing style with the median price and sales count for each band, and a rule line. Bands include their lower edge (a home at exactly 3.0 miles is in "3 to 5 miles"). The README's rerun list includes the new script.
- **Checked or changed:** Ran the script twice and got the same file. The five band counts (1,491, 12,888, 11,217, 9,561 and 245) add up to the 35,402 sales of $10,000 or more, and the medians matched a separate check. In a headless browser at phone and desktop widths the page had no horizontal scroll and no console errors. The agent's first phone render had the axis labels crowding together ("$400k$600k"), so I changed the axis to $0, $300k and $600k.

## 2026-11-19: Final check, README and log

- **Asked:** "Read AGENTS.md and docs/data_description_sheet.md again do a final check: rerun every script and confirm every number on the page matches the JSON files and the data. List any mismatch and fix it. Make sure all paths are relative and file name case matches exactly. Fill in the README sections from the template, describing the site and the data rules used. Then add dated entries to AGENT_LOG.md for each task in this session, using the outline in that file, including the exact prompts I gave you and one thing that needed fixing (the $876,985.5 median that wasn't rounded)."
- **Agent produced:** Reran all four scripts. Each JSON file came out byte-identical to the committed file. Recomputed every figure on the page from the CSV and from the SQLite file, with no mismatches between the two sources. Rendered the page at desktop and phone widths: no console errors, no failed requests, no horizontal scroll. Filled in the README from its template, with the rules used and the five data problems. Added the entries in this log.
- **Checked or changed:** Mismatches found and fixed:
  - The README said the site reads two JSON files. It reads four.
  - The README said the site reads the CSV. It reads JSON files made from the CSV.
  - The README said "Claud Code" and the placeholder text was still there. Fixed.
  - `scripts/README.md` said the CSV is 9 MB. It is 8.7 MB. Fixed.
  - Checked, not changed: the data description sheet's city table uses sales of $1,000 or more, and the page uses $10,000. Ann Arbor is $571,000 in the sheet and $572,000 on the page. The README now says so.
  - Paths are all relative, and every file name matches its case. The live site could not be reached from the agent's sandbox, so the live URL in the README has not been confirmed in a browser.
