import pandas as pd

input_file = "../data/compact.csv"
output_file = "../data/epidemic_data_cleaned.csv"

df = pd.read_csv(input_file)

df_filtered = df[df['country'].isin(['France', 'Europe'])].copy()

columns_to_keep = [
    'country',                          
    'date',                             
    'new_cases_smoothed_per_million',   
    'new_deaths_smoothed_per_million',  
    'total_vaccinations_per_hundred',   
    'total_cases',                      
    'total_deaths'                      
]
df_cleaned = df_filtered[columns_to_keep].copy()

df_cleaned = df_cleaned.sort_values(by=['country', 'date']).reset_index(drop=True)

df_cleaned['total_vaccinations_per_hundred'] = (
    df_cleaned.groupby('country')['total_vaccinations_per_hundred']
    .ffill()
    .fillna(0)
)

df_cleaned['new_cases_smoothed_per_million'] = df_cleaned['new_cases_smoothed_per_million'].fillna(0)
df_cleaned['new_deaths_smoothed_per_million'] = df_cleaned['new_deaths_smoothed_per_million'].fillna(0)

df_cleaned['total_cases'] = df_cleaned.groupby('country')['total_cases'].ffill().fillna(0)
df_cleaned['total_deaths'] = df_cleaned.groupby('country')['total_deaths'].ffill().fillna(0)

df_cleaned.to_csv(output_file, index=False)






