import pandas as pd
import os


raw_data_dir = "data/raw"
output_dir = "data/raw"  


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


qs_countries = sorted(qs['Country'].unique())

missing_data = {
    "Country": [],
    "Education_Spending_Missing": [],
    "GDP_Missing": [],
    "Population_Missing": []
}

for country in qs_countries:
    edu_missing = is_recent_data_missing(edu, 'Country Name', country, recent_years)
    gdp_missing = is_recent_data_missing(gdp, 'Country Name', country, recent_years)
    pop_missing = is_recent_data_missing(pop, 'Country Name', country, recent_years)

    
    missing_data["Country"].append(country)
    missing_data["Education_Spending_Missing"].append("Yes" if edu_missing else "No")
    missing_data["GDP_Missing"].append("Yes" if gdp_missing else "No")
    missing_data["Population_Missing"].append("Yes" if pop_missing else "No")


missing_df = pd.DataFrame(missing_data)


output_path = os.path.join(output_dir, "manual_supplement_template.csv")
missing_df.to_csv(output_path, index=False)

print(f"Manual supplement template saved to: {output_path}")
print(missing_df)
