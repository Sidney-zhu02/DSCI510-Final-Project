import pandas as pd
import os
import requests
import time


project_root = "/root/DSCI510-Final-Project"
processed_dir = os.path.join(project_root, "data", "processed")
os.makedirs(processed_dir, exist_ok=True)


edu_df = pd.read_csv(os.path.join(processed_dir, "education_expenditure_completed.csv"))
gdp_df = pd.read_csv(os.path.join(processed_dir, "gdp_cleaned.csv"))
pop_df = pd.read_csv(os.path.join(processed_dir, "population_cleaned.csv"))
qs_df = pd.read_csv(os.path.join(processed_dir, "qs_top100_cleaned.csv"))


qs_countries = qs_df["Country Name"].unique().tolist()

country_name_to_iso2 = {
    'Argentina': 'AR', 'Australia': 'AU', 'Belgium': 'BE', 'Canada': 'CA', 'China (Mainland)': 'CN',
    'Denmark': 'DK', 'France': 'FR', 'Germany': 'DE', 'Japan': 'JP', 'Netherlands': 'NL',
    'New Zealand': 'NZ', 'Russia': 'RU', 'Singapore': 'SG', 'South Korea': 'KR', 'Sweden': 'SE',
    'Switzerland': 'CH', 'Taiwan': 'TW', 'United Kingdom': 'GB', 'United States': 'US',
    'Malaysia': 'MY', 'Hong Kong SAR': 'HK'
}

YEARS = [2018, 2019, 2020, 2021, 2022]


def fetch_country_indicator(iso2_code, indicator):
    """Fetch data from World Bank API"""
    url = f"https://api.worldbank.org/v2/country/{iso2_code}/indicator/{indicator}?format=json&per_page=500"
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
        return dict(records)
    except Exception:
        return {}

def get_taiwan_timeseries(field):
    """Manual fill Taiwan"""
    if field == 'gdp':
        return {2018: 550e9, 2019: 600e9, 2020: 650e9, 2021: 700e9, 2022: 760e9}
    elif field == 'population':
        return {2018: 23300000, 2019: 23350000, 2020: 23400000, 2021: 23450000, 2022: 23500000}
    elif field == 'education_spending':
        return {2018: 5.8, 2019: 5.8, 2020: 5.9, 2021: 6.0, 2022: 6.0}
    return {}

def get_manual_hk_my(field, country):
    """Manual fill Hong Kong and Malaysia education expenditure"""
    if field == "education_spending":
        if country == "Hong Kong SAR":
            return {2018: 3.3, 2019: 3.8, 2020: 3.9, 2021: 3.7, 2022: 3.7}
        elif country == "Malaysia":
            return {2018: 4.5, 2019: 4.5, 2020: 4.4, 2021: 4.3, 2022: 4.3}
    return {}


rows = []

for country in qs_countries:
    iso2 = country_name_to_iso2.get(country, "")
    for year in YEARS:
        row = {"Country Name": country, "Country Code": iso2, "Year": year}

        if country == "China (Mainland)":
            gdp_records = fetch_country_indicator("CN", "NY.GDP.MKTP.CD")
            pop_records = fetch_country_indicator("CN", "SP.POP.TOTL")
            edu_records = fetch_country_indicator("CN", "SE.XPD.TOTL.GD.ZS")
            time.sleep(1)
            row["GDP (current US$)"] = gdp_records.get(year)
            row["Population"] = pop_records.get(year)
            row["Education Expenditure (% of GDP)"] = edu_records.get(year)

        elif country == "Taiwan":
            row["GDP (current US$)"] = get_taiwan_timeseries("gdp").get(year)
            row["Population"] = get_taiwan_timeseries("population").get(year)
            row["Education Expenditure (% of GDP)"] = get_taiwan_timeseries("education_spending").get(year)

        else:
            gdp_val = gdp_df.query("`Country Name` == @country and Year == @year")["Value"]
            pop_val = pop_df.query("`Country Name` == @country and Year == @year")["Value"]
            edu_val = edu_df.query("`Country Name` == @country and Year == @year")["Value"]

            row["GDP (current US$)"] = gdp_val.values[0] if not gdp_val.empty else None
            row["Population"] = pop_val.values[0] if not pop_val.empty else None

            if not edu_val.empty:
                row["Education Expenditure (% of GDP)"] = edu_val.values[0]
            else:
    
                if country in ["Hong Kong SAR", "Malaysia"]:
                    row["Education Expenditure (% of GDP)"] = get_manual_hk_my("education_spending", country).get(year)
                else:
                    row["Education Expenditure (% of GDP)"] = None

        rows.append(row)


final_df = pd.DataFrame(rows)

for col in ["GDP (current US$)", "Population", "Education Expenditure (% of GDP)"]:
    final_df[col] = final_df.groupby("Country Name")[col].transform(lambda x: x.interpolate(limit_direction="both"))


final_output_path = os.path.join(processed_dir, "final_merged_data_complete.csv")
final_df.to_csv(final_output_path, index=False)

print(f" Final merged data saved to: {final_output_path}")





