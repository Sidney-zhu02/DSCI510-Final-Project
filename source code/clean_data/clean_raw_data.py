import pandas as pd
import os


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
raw_dir = os.path.join(project_root, 'data', 'raw')
processed_dir = os.path.join(project_root, 'data', 'processed')
os.makedirs(processed_dir, exist_ok=True)

def melt_and_clean(file_path, value_name, apply_value_range=False, value_range=(0, 10)):
    df = pd.read_csv(file_path)

    
    id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
    year_columns = [col for col in df.columns if col not in id_vars]
    df_melted = df.melt(id_vars=id_vars, value_vars=year_columns, var_name='Year', value_name='Value')

   
    df_melted = df_melted[['Country Name', 'Country Code', 'Year', 'Value']]

    
    df_melted = df_melted.dropna(subset=['Country Name', 'Year', 'Value'])
    df_melted['Year'] = pd.to_numeric(df_melted['Year'], errors='coerce')
    df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')

    
    df_melted = df_melted[df_melted['Year'].between(2018, 2022)]

    
    if apply_value_range:
        df_melted = df_melted[df_melted['Value'].between(*value_range)]

    
    df_melted = df_melted[df_melted['Value'] > 0]

    df_melted = df_melted.drop_duplicates()

    return df_melted

def clean_qs_file(file_path):
    df = pd.read_csv(file_path)
    df = df.rename(columns={'Country': 'Country Name'})
    df = df.dropna(subset=['Country Name'])
    df['Country Name'] = df['Country Name'].str.strip()
    df = df.drop_duplicates()
    return df

def main():
    edu_path = os.path.join(raw_dir, 'education_expenditure.csv')
    gdp_path = os.path.join(raw_dir, 'gdp.csv')
    pop_path = os.path.join(raw_dir, 'population.csv')
    qs_path = os.path.join(raw_dir, 'qs_top100.csv')

    edu_clean = melt_and_clean(edu_path, value_name='Education Expenditure (% of GDP)', apply_value_range=True, value_range=(0, 10))
    gdp_clean = melt_and_clean(gdp_path, value_name='GDP (current US$)', apply_value_range=False)
    pop_clean = melt_and_clean(pop_path, value_name='Population', apply_value_range=False)
    qs_clean = clean_qs_file(qs_path)

    edu_clean.to_csv(os.path.join(processed_dir, 'education_expenditure_cleaned.csv'), index=False)
    gdp_clean.to_csv(os.path.join(processed_dir, 'gdp_cleaned.csv'), index=False)
    pop_clean.to_csv(os.path.join(processed_dir, 'population_cleaned.csv'), index=False)
    qs_clean.to_csv(os.path.join(processed_dir, 'qs_top100_cleaned.csv'), index=False)

    print(" Raw data cleaned and saved to /data/processed/")

if __name__ == "__main__":
    main()
