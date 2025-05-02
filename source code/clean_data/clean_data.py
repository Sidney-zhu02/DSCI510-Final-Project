import pandas as pd
import os

def clean_education_data(df):
    df = df.dropna(subset=['Country Name'])
    df['Country Name'] = df['Country Name'].str.strip()
    df = df[(df['Value'] >= 0) & (df['Value'] <= 10)]
    df = df.drop_duplicates()
    return df

def clean_gdp_data(df):
    df = df.dropna(subset=['Country Name'])
    df['Country Name'] = df['Country Name'].str.strip()
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')  
    df = df[df['Value'] > 0]
    df = df.drop_duplicates()
    return df

def clean_population_data(df):
    df = df.dropna(subset=['Country Name'])
    df['Country Name'] = df['Country Name'].str.strip()
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df = df[df['Value'] > 0]
    df = df.drop_duplicates()
    return df

def clean_qs_data(df):
    df = df.rename(columns={'Country': 'Country Name'})  
    df = df.dropna(subset=['Country Name'])
    df['Country Name'] = df['Country Name'].str.strip()
    df = df.drop_duplicates()
    return df

def main():
    raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw'))
    processed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed'))
    os.makedirs(processed_dir, exist_ok=True)

    
    edu_df = pd.read_csv(os.path.join(raw_dir, 'education_expenditure_completed.csv'))
    

    gdp_path = os.path.join(processed_dir, 'gdp_completed_fixed.csv')
    pop_path = os.path.join(processed_dir, 'population_completed_fixed.csv')

    if os.path.exists(gdp_path) and os.path.exists(pop_path):
        gdp_df = pd.read_csv(gdp_path)
        pop_df = pd.read_csv(pop_path)
        print("Using fixed GDP and Population files.")
    else:
        gdp_df = pd.read_csv(os.path.join(raw_dir, 'gdp_completed.csv'))
        pop_df = pd.read_csv(os.path.join(raw_dir, 'population_completed.csv'))
        print("Using original GDP and Population files (fixed versions not found).")

    qs_df = pd.read_csv(os.path.join(raw_dir, 'qs_top100.csv'))

   
    edu_clean = clean_education_data(edu_df)
    gdp_clean = clean_gdp_data(gdp_df)
    pop_clean = clean_population_data(pop_df)
    qs_clean = clean_qs_data(qs_df)

    
    edu_clean.to_csv(os.path.join(processed_dir, 'education_expenditure_cleaned.csv'), index=False)
    gdp_clean.to_csv(os.path.join(processed_dir, 'gdp_cleaned.csv'), index=False)
    pop_clean.to_csv(os.path.join(processed_dir, 'population_cleaned.csv'), index=False)
    qs_clean.to_csv(os.path.join(processed_dir, 'qs_top100_cleaned.csv'), index=False)

    print("\n Data cleaning completed! Cleaned datasets saved in /data/processed/")

if __name__ == "__main__":
    main()
