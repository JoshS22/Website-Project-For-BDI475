# Agent log

Add a dated entry each time you work with your AI coding agent, with the newest entry at the bottom. Each entry records what you asked the agent, what it produced, and what you checked or changed. Paste your key prompts in exactly as you typed them. Include at least one time the agent got something wrong, and how you caught it.

Copy this outline for each entry:

```markdown
## YYYY-MM-DD: What you worked on

- **Asked:** "Paste your prompt here."
- **Agent produced:** What it made or changed.
- **Checked or changed:** How you checked it, and what you fixed.
```

## 2026-11-19: University of Illinois area section

- **Asked:** "Read AGENTS.md and docs/data_description_sheet.md again. Add a section about the University of Illinois area (Champaign, Urbana, Savoy). Using a script in scripts/ that writes a new JSON file in data/, compute for each university: number of sales, median sale price (sales of $10,000 or more), and median days on market, calculated as contract_date minus list_date only on rows that have both dates. Never treat a blank date as zero, and use the median, not the mean. Show this as a table or bar chart, highlight the University of Illinois row, and add a note saying how many rows had both dates. Tell me how to check it."
- **Agent produced:** `scripts/make_university_summary.py`, which writes `data/university_summary.json`. A table of all 11 universities with the Illinois row highlighted, a note giving the count of rows with both dates, and a table of Champaign, Urbana and Savoy. The page's rule line now says the $10,000 rule applies to median prices, since the sales count includes every sale.
- **Checked or changed:** Ran the script twice and got the same file. The 11 sales counts add up to all 35,442 rows, and the both-dates count (28,042) and same-day count (384) match the data description sheet. The Illinois figures were recomputed from the SQLite file and matched.
