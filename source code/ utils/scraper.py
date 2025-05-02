import requests
import pandas as pd
import argparse
from bs4 import BeautifulSoup

API_URL = "https://www.topuniversities.com/sites/default/files/qs-rankings-data/en/3740566.txt"

def clean_university_name(html_str):
    try:
        return BeautifulSoup(html_str, "html.parser").get_text(strip=True)
    except:
        return html_str

def fetch_qs_top100():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        raw_data = resp.json()
        universities = raw_data['data']

        data = []
        for entry in universities[:100]:
            rank = entry.get('rank_display', '').strip()
            raw_title = entry.get('title', '').strip()
            university = clean_university_name(raw_title)
            country = entry.get('country', '').strip()
            data.append([rank, university, country])

        df = pd.DataFrame(data, columns=["Rank", "University", "Country"])
        return df

    except Exception as e:
        print(f"Error while scraping: {e}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scrape', type=int, help='Scrape only N rows')
    parser.add_argument('--save', type=str, help='Save CSV to file path')
    args = parser.parse_args()

    df = fetch_qs_top100()
    if df is None or df.empty:
        print("No data scraped.")
        return

    if args.scrape:
        print(df.head(args.scrape).to_string(index=False))
    elif args.save:
        df.to_csv(args.save, index=False)
        print(f"Data saved to {args.save}")
    else:
        print(df.to_string(index=False))

    print(f"Total universities scraped: {len(df)}")

if __name__ == "__main__":
    main()
