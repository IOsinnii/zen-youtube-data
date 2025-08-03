import os
import pandas as pd
import json

# Read the JSON file
with open('../input/dataset_youtube-scraper-task_2025-04-26.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Remove some columns
df = df.drop(['order','thumbnailUrl','date','id','url','duration'], axis=1)
# Rename columns for clarity, "text" to "description"
df = df.rename(columns={"text": "description"})

# Ensure output directory exists
os.makedirs('../output', exist_ok=True)

# Optional: Save the cleaned DataFrame to CSV
df.to_csv('../output/01_title_description_cleaned.csv', index=False, encoding='utf-8-sig', sep=';')
print("\nDataFrame saved to '01_title_description_cleaned.csv'")

# Convert the DataFrame back to JSON   
df_records = df.to_dict(orient='records')

# Optional: Save the JSON to a file
with open('../output/01_title_description_cleaned.json', 'w', encoding='utf-8') as json_file:
    json.dump(df_records, json_file, ensure_ascii=False, indent=4)
