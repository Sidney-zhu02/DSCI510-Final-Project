# DSCI 510 Project - Submission 2
"Does Spending More on Education Lead to Better Global University Rankings?"  
Author: Hengxiao Zhu (zhuhengx@usc.edu)
============================================================================

## Objective:

This script extracts and processes data to investigate whether countries that invest a greater share of GDP in education are more likely to have universities ranked in the QS World University Rankings Top 100.

This submission focuses on:
1. Extracting data from the most complex source: QS World University Rankings 2024
2. Presenting an ER diagram to model the relationships across all three data sources


## Files included in this submission:

1. `scraper.py`
   - A Python script that scrapes the QS Top 100 rankings from:
     https://www.topuniversities.com/university-rankings/world-university-rankings/2024
   - Outputs a list of universities with rank, university name, and country.

2. `qs_rankings.csv`
   - A static version of the scraped QS data, listing rank, university, and country.

3. `data models.drawio.pdf`
   - Entity-Relationship (ER) diagram showing the relationships among:
     - QS Rankings
     - World Bank Education Spending (% of GDP)
     - World Bank GDP & Population


## How to Run the Script:

Option 1: Run and display full QS Top 100 university rankings
- python scraper.py

Option 2: Only display top N rows (e.g., top 10)
- python scraper.py --scrape 10

Option 3: Save the full dataset to a CSV file
- python scraper.py --save qs_rankings.csv

## Data Schema Overview:

1. qs_rankings
- country: Country name
- num_top100: Number of QS Top 100 universities per country
- year: Ranking year (e.g., 2024)

2. education_spending
- country: Country name
- avg_spending_pct_gdp: Average education spending (% of GDP) over past 5 years
- year: Year range (e.g., 2018–2022)

3. country_info
- country: Country name
- gdp: GDP (USD)
- population: Population size
- year: Same year as QS ranking

4. Notes:
- Static data is stored in the current directory as qs_rankings.csv  
- Education and GDP/Population datasets will be integrated in the next phase  

