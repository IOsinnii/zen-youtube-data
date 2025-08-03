import pandas as pd
import json

# Load the processed data from script 3
with open('../output/03b_lectures_with_reformatted_dates.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

print("Loaded DataFrame shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nSample data:")
print(df[['title', 'number', 'date', 'date_standard']].head())

def extract_lecture_part(number_str):
    """Extract lecture number and part from format like '126-2' or plain number"""
    if pd.isna(number_str) or number_str is None:
        return 0, 0  # For lectures without numbers
    
    number_str = str(number_str)
    if '-' in number_str:
        # Format like '126-2'
        parts = number_str.split('-')
        try:
            lecture_num = int(parts[0])
            part_num = int(parts[1])
            return lecture_num, part_num
        except (ValueError, IndexError):
            return 0, 0
    else:
        # Plain number like '126'
        try:
            lecture_num = int(number_str)
            return lecture_num, 0  # No part number
        except ValueError:
            return 0, 0

print("\nPreparing data for sorting...")

# Process dates for sorting
if 'date_standard' in df.columns:
    print("Using standardized dates from script 3")
    df['date_datetime'] = pd.to_datetime(df['date_standard'], format='%d/%m/%Y', errors='coerce')
elif 'date' in df.columns:
    print("Using original date column")
    df['date_datetime'] = pd.to_datetime(df['date'], errors='coerce')
    df['date_standard'] = df['date_datetime'].dt.strftime('%d/%m/%Y')
else:
    print("No date columns found!")
    df['date_datetime'] = pd.NaT
    df['date_standard'] = None

# Extract lecture and part numbers
print("Extracting lecture numbers and parts...")
df['lecture_num'], df['part_num'] = zip(*df['number'].apply(extract_lecture_part))

# Report preparation results
valid_dates = df['date_datetime'].notna().sum()
total_rows = len(df)
lectures_with_numbers = df['number'].notna().sum()

print(f"\nPreparation Results:")
print(f"Total lectures: {total_rows}")
print(f"Valid dates: {valid_dates}")
print(f"Lectures with numbers: {lectures_with_numbers}")
print(f"Lectures without numbers: {total_rows - lectures_with_numbers}")

# Show examples of extracted numbers
print(f"\nSample number extractions:")
sample_df = df[['title', 'number', 'lecture_num', 'part_num']].head(10)
for _, row in sample_df.iterrows():
    if pd.notna(row['number']):
        print(f"  '{row['number']}' → Lecture: {row['lecture_num']}, Part: {row['part_num']}")

# Save prepared data
output_file = '../output/4a_lectures_prepared_for_sorting.json'

# Convert DataFrame to records, handling datetime objects
df_for_json = df.copy()
# Convert datetime objects to strings for JSON serialization
df_for_json['date_datetime'] = df_for_json['date_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

df_records = df_for_json.to_dict(orient='records')

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(df_records, json_file, ensure_ascii=False, indent=4)


print(f"\nPrepared data saved to: {output_file}")
print(f"Next step: Run 4b_create_chronological_order.py to create final ordering")
