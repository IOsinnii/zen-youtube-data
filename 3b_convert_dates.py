import pandas as pd
import json
from dateutil.parser import parse

# Load the data and analysis results
with open('output/02_lectures_with_extracted_info.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('output/date_format_analysis.json', 'r', encoding='utf-8') as file:
    analysis = json.load(file)

df = pd.DataFrame(data)

print("Loaded DataFrame shape:", df.shape)
print(f"Analysis results: {analysis['detected_format']} format detected")
print(f"Conversion needed: {analysis['needs_conversion']}")

# Russian month mapping
russian_months = {
    'января': 'January', 'февраля': 'February', 'марта': 'March',
    'апреля': 'April', 'мая': 'May', 'июня': 'June',
    'июля': 'July', 'августа': 'August', 'сентября': 'September',
    'октября': 'October', 'ноября': 'November', 'декабря': 'December'
}

print("\nPerforming date conversion...")

if analysis['needs_conversion']:
    # Convert from Russian format
    print("Converting from Russian date format to DD/MM/YYYY...")
    
    def convert_russian_date_advanced(date_str):
        """Convert Russian date to DD/MM/YYYY format"""
        if pd.isna(date_str) or date_str is None:
            return None, None
        
        try:
            # Clean and prepare the date string
            date_str = str(date_str).strip()
            
            # Replace Russian month names with English
            english_date = date_str
            for ru_month, en_month in russian_months.items():
                english_date = english_date.replace(ru_month, en_month)
            
            # Parse the date
            parsed_date = parse(english_date)
            date_standard = parsed_date.strftime('%d/%m/%Y')
            
            return parsed_date, date_standard
            
        except Exception as e:
            return None, None
    
    # Apply conversion
    print("Processing all dates...")
    conversion_results = df['date'].apply(convert_russian_date_advanced)
    df['date_datetime'] = [result[0] for result in conversion_results]
    df['date_standard'] = [result[1] for result in conversion_results]
    
else:
    # Already in DD/MM/YYYY format
    print("Dates already in DD/MM/YYYY format - validating...")
    df['date_standard'] = df['date'].astype(str)
    df['date_datetime'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

# Report results
successful_conversions = df['date_datetime'].notna().sum()
total_dates = df['date'].notna().sum()

print(f"\nConversion Results:")
print(f"Total dates: {total_dates}")
print(f"Successfully processed: {successful_conversions}")
print(f"Failed conversions: {total_dates - successful_conversions}")
print(f"Success rate: {(successful_conversions/total_dates*100):.1f}%" if total_dates > 0 else "N/A")

# Show failed conversions
failed_dates = df[df['date'].notna() & df['date_datetime'].isna()]
if len(failed_dates) > 0:
    print(f"\nFailed conversions ({len(failed_dates)}):")
    for idx, row in failed_dates.head(5).iterrows():
        print(f"  - '{row['date']}' in '{row['title']}'")
    if len(failed_dates) > 5:
        print(f"  ... and {len(failed_dates) - 5} more")

# Clean up and save
df_export = df.drop(columns=['date_datetime'], errors='ignore')

output_file = 'output/lectures_with_reformatted_dates.json'
df_records = df_export.to_dict(orient='records')

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(df_records, json_file, ensure_ascii=False, indent=4)

print(f"\nData saved to: {output_file}")

# Also save CSV
df_export.to_csv('output/lectures_with_reformatted_dates.csv', index=False, encoding='utf-8-sig', sep=';')
print("Also saved as CSV: output/lectures_with_reformatted_dates.csv")

print(f"\nNext step: Run 4a_prepare_sorting.py to prepare for chronological ordering")
