import os
import requests
import pandas as pd


RAW_DATA_DIR = "/root/DSCI510-Final-Project/data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)


BASE_URL = "http://api.worldbank.org/v2/en/indicator/{indicator}?downloadformat=csv"


INDICATORS = {
    "education_expenditure": "SE.XPD.TOTL.GD.ZS",  
    "gdp": "NY.GDP.MKTP.CD",                      
    "population": "SP.POP.TOTL"                   
}

def download_and_extract(indicator_name, indicator_code):
    """CSV download and extract data from world bank API."""
    print(f"Downloading {indicator_name}...")
    url = BASE_URL.format(indicator=indicator_code)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download {indicator_name}: {response.status_code}")

    from io import BytesIO
    from zipfile import ZipFile

    zipfile = ZipFile(BytesIO(response.content))
    file_list = zipfile.namelist()
    
    
    data_file = None
    for filename in file_list:
        if filename.startswith("API_") and filename.endswith(".csv"):
            data_file = filename
            break
    if not data_file:
        raise Exception(f"No valid data CSV found for {indicator_name}")
    
    
    df = pd.read_csv(zipfile.open(data_file), skiprows=4)
    print(f"{indicator_name} data shape: {df.shape}")

    
    save_path = os.path.join(RAW_DATA_DIR, f"{indicator_name}.csv")
    df.to_csv(save_path, index=False)
    print(f"{indicator_name} saved to {save_path}")

def main():
    for name, code in INDICATORS.items():
        try:
            download_and_extract(name, code)
        except Exception as e:
            print(f"Error downloading {name}: {e}")

if __name__ == "__main__":
    main()
