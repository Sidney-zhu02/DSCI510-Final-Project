import pandas as pd
import requests
import os
import time


country_name_to_iso2 = {
    'Argentina': 'AR',
    'Australia': 'AU',
    'Belgium': 'BE',
    'Canada': 'CA',
    'China (Mainland)': 'CN',
    'Denmark': 'DK',
    'France': 'FR',
    'Germany': 'DE',
    'Japan': 'JP',
    'Netherlands': 'NL',
    'New Zealand': 'NZ',
    'Russia': 'RU',
    'Singapore': 'SG',
    'South Korea': 'KR',
    'Sweden': 'SE',
    'Switzerland': 'CH',
    'Taiwan': 'TW',  
    'United Kingdom': 'GB',
    'United States': 'US'
}


INDICATOR = 'SE.XPD.TOTL.GD.ZS'


YEARS = [2018, 2019, 2020, 2021, 2022]


def fetch_education_spending(iso2_code):
    url = f"https://api.worldbank.org/v2/country/{iso2_code}/indicator/{INDICATOR}?format=json&per_page=500"
    try:
        response = requests.get(url)
        data = response.json()
        records = []
        if isinstance(data, list) and len(data) >= 2:
            for record in data[1]:
                year = int(record.get('date'))
                value = record.get('value')
                if year in YEARS:
                    records.append((year, value))
        return records
    except Exception as e:
        print(f"Error fetching education expenditure for {iso2_code}: {e}")
        return []


def get_taiwan_education_timeseries():
    return [
        (2022, 6.0),
        (2021, 6.0),
        (2020, 5.9),
        (2019, 5.8),
        (2018, 5.8)
    ]

def main():
    processed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed'))
    os.makedirs(processed_dir, exist_ok=True)

    edu_data = []

    for country, iso2 in country_name_to_iso2.items():
        print(f"Fetching education expenditure for {country}...")
        if country == 'Taiwan':
            records = get_taiwan_education_timeseries()
        else:
            records = fetch_education_spending(iso2)
            time.sleep(1)  
        
        for year, value in records:
            edu_data.append({
                'Country Name': country,
                'Country Code': iso2,
                'Year': year,
                'Value': value
            })

    
    edu_df = pd.DataFrame(edu_data)

    
    complete_index = pd.MultiIndex.from_product(
        [list(country_name_to_iso2.keys()), YEARS],
        names=['Country Name', 'Year']
    )
    edu_df = edu_df.set_index(['Country Name', 'Year']).reindex(complete_index).reset_index()

    
    edu_df['Country Code'] = edu_df['Country Name'].map(country_name_to_iso2)

    
    edu_df.to_csv(os.path.join(processed_dir, 'education_expenditure_completed.csv'), index=False)

    print("\n Education expenditure data fetch & completion done!")
    print("Saved to: /data/processed/education_expenditure_completed.csv")

if __name__ == "__main__":
    main()
