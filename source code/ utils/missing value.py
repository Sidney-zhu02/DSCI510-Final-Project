import pandas as pd
import os


raw_data_dir = "data/raw"


qs = pd.read_csv(os.path.join(raw_data_dir, "qs_top100.csv"))  
edu = pd.read_csv(os.path.join(raw_data_dir, "education_expenditure.csv"))
gdp = pd.read_csv(os.path.join(raw_data_dir, "gdp.csv"))
pop = pd.read_csv(os.path.join(raw_data_dir, "population.csv"))


recent_years = ['2018', '2019', '2020', '2021', '2022']


def is_recent_data_missing(df, country_col, target_country, years):
    row = df[df[country_col] == target_country]
    if row.empty:
        return True  
    recent_values = row[years].values.flatten()
    return pd.isna(recent_values).all()


missing_edu = []
missing_gdp = []
missing_pop = []


qs_countries = sorted(qs['Country'].unique())


for country in qs_countries:
    if is_recent_data_missing(edu, 'Country Name', country, recent_years):
        missing_edu.append(country)
    if is_recent_data_missing(gdp, 'Country Name', country, recent_years):
        missing_gdp.append(country)
    if is_recent_data_missing(pop, 'Country Name', country, recent_years):
        missing_pop.append(country)


print(f"\nTotal QS countries: {len(qs_countries)}")

print("\nCountries missing Education Spending data:")
print(missing_edu)

print("\nCountries missing GDP data:")
print(missing_gdp)

print("\nCountries missing Population data:")
print(missing_pop)

