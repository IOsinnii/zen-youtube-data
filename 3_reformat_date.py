import pandas as pd
import json
from dateutil.parser import parse

# Load the JSON file with extracted lecture information
with open('output/02_lectures_with_extracted_info.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Display basic info about the loaded data
print("Loaded DataFrame shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nOriginal data:")
print(df[['title', 'number', 'date']].head())

# Create a mapping for Russian months to English
russian_months = {
    'января': 'January', 'февраля': 'February', 'марта': 'March',
    'апреля': 'April', 'мая': 'May', 'июня': 'June',
    'июля': 'July', 'августа': 'August', 'сентября': 'September',
    'октября': 'October', 'ноября': 'November', 'декабря': 'December'
}

def convert_russian_date(date_str):
    """Convert Russian date format to DD/MM/YYYY"""
    if pd.isna(date_str) or date_str is None:
        return None
    
    try:
        # Replace Russian month names with English
        english_date = str(date_str)
        for ru_month, en_month in russian_months.items():
            english_date = english_date.replace(ru_month, en_month)
        
        # Parse the date and format as DD/MM/YYYY
        parsed_date = parse(english_date)
        return parsed_date.strftime('%d/%m/%Y')
        
    except Exception as e:
        print(f"Error converting date '{date_str}': {e}")
        return None

# Advanced date conversion logic (adapted from script 4)
print("\nAnalyzing date format and converting to standard DD/MM/YYYY...")

if 'date' in df.columns:
    # Check if dates are already in DD/MM/YYYY format
    sample_dates = df['date'].dropna().head(5) if not df['date'].dropna().empty else []
    
    # Analyze sample dates to detect format
    dd_mm_yyyy_count = 0
    russian_format_count = 0
    
    for sample_date in sample_dates:
        if '/' in str(sample_date):
            dd_mm_yyyy_count += 1
        elif any(month in str(sample_date) for month in russian_months.keys()):
            russian_format_count += 1
    
    print(f"Date format analysis: {dd_mm_yyyy_count} DD/MM/YYYY, {russian_format_count} Russian format")
    
    if dd_mm_yyyy_count > russian_format_count:
        # Already in DD/MM/YYYY format
        print("Dates appear to be in DD/MM/YYYY format - keeping as-is")
        df['date_standard'] = df['date'].astype(str)
        # Create datetime column for validation
        df['date_datetime'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
    else:
        # Convert from Russian format
        print("Converting from Russian date format...")
        
        def convert_russian_date_advanced(date_str):
            """Advanced Russian date conversion with better error handling"""
            if pd.isna(date_str) or date_str is None:
                return None, None
            
            try:
                # Clean up the date string
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
                print(f"Warning: Could not parse date '{date_str}': {e}")
                return None, None
        
        # Apply conversion
        conversion_results = df['date'].apply(convert_russian_date_advanced)
        df['date_datetime'] = [result[0] for result in conversion_results]
        df['date_standard'] = [result[1] for result in conversion_results]
        
    # Report conversion results
    successful_conversions = df['date_datetime'].notna().sum()
    total_dates = df['date'].notna().sum()
    print(f"Date processing: {successful_conversions}/{total_dates} successful")
    
    # Handle failed conversions
    failed_dates = df[df['date'].notna() & df['date_datetime'].isna()]
    if len(failed_dates) > 0:
        print(f"\nFailed conversions ({len(failed_dates)}):")
        for idx, row in failed_dates.head(5).iterrows():
            print(f"  - '{row['date']}' in '{row['title']}'")
        if len(failed_dates) > 5:
            print(f"  ... and {len(failed_dates) - 5} more")
            
else:
    print("No date column found!")
    df['date_datetime'] = pd.NaT
    df['date_standard'] = None

# Display results
print("\nConversion results:")
print("="*60)
for idx, row in df.head(10).iterrows():  # Show only first 10 for readability
    print(f"Title: {row['title']}")
    print(f"Number: {row['number']}")
    print(f"Original Date: {row['date']}")
    print(f"Standard Date: {row['date_standard']}")
    print("-" * 40)

if len(df) > 10:
    print(f"... and {len(df) - 10} more lectures")

# Show summary
successful_conversions = df['date_standard'].notna().sum()
total_dates = df['date'].notna().sum()
print(f"\nConversion Summary:")
print(f"Total dates found: {total_dates}")
print(f"Successfully converted: {successful_conversions}")
print(f"Failed conversions: {total_dates - successful_conversions}")
print(f"Success rate: {(successful_conversions/total_dates*100):.1f}%" if total_dates > 0 else "N/A")

# Show the final DataFrame structure
print(f"\nFinal DataFrame columns: {df.columns.tolist()}")
sample_df = df[['title', 'number', 'date', 'date_standard']].head()
print(f"\nSample data:")
print(sample_df)

# Clean up temporary datetime column for export
df_export = df.drop(columns=['date_datetime'], errors='ignore')

# Save the enhanced DataFrame with reformatted dates
output_file = 'output/lectures_with_reformatted_dates.json'
df_records = df_export.to_dict(orient='records')

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(df_records, json_file, ensure_ascii=False, indent=4)

print(f"\nEnhanced data saved to: {output_file}")

# Optional: Save as CSV for easier viewing with proper encoding
df_export.to_csv('output/lectures_with_reformatted_dates.csv', index=False, encoding='utf-8-sig', sep=';')
print("Also saved as CSV: output/lectures_with_reformatted_dates.csv")
