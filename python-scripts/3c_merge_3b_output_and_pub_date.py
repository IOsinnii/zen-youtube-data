# so far just to convert .xlsx to .json 
import json
import pandas as pd

# load the data

df = pd.read_excel('../input/lectures_experimental_order', engine='openpyxl')

# Convert DataFrame to JSON format

df_records = df.to_dict(orient='records')

# Save the DataFrame to a JSON file
output_file = '../output/lectures_experimental_order.json'
with open(output_file, 'w') as f:
    json.dump(df_records, f, indent=4)
