import pandas as pd
import json

# Load the JSON file with extracted lecture information from script 2
with open('output/02_lectures_with_extracted_info.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Display basic info about the loaded data
print("Loaded DataFrame shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df[['title', 'number', 'date']].head())

# Russian month mapping for detection
russian_months = {
    'января': 'January', 'февраля': 'February', 'марта': 'March',
    'апреля': 'April', 'мая': 'May', 'июня': 'June',
    'июля': 'July', 'августа': 'August', 'сентября': 'September',
    'октября': 'October', 'ноября': 'November', 'декабря': 'December'
}

# Analyze date format
print("\nAnalyzing date formats...")

if 'date' in df.columns:
    # Get sample dates for analysis
    sample_dates = df['date'].dropna().head(10) if not df['date'].dropna().empty else []
    
    # Count different format types
    dd_mm_yyyy_count = 0
    russian_format_count = 0
    other_format_count = 0
    
    print(f"\nAnalyzing {len(sample_dates)} sample dates:")
    for i, sample_date in enumerate(sample_dates):
        date_str = str(sample_date)
        print(f"  {i+1}. '{date_str}'", end=" - ")
        
        if '/' in date_str and len(date_str.split('/')) == 3:
            dd_mm_yyyy_count += 1
            print("DD/MM/YYYY format")
        elif any(month in date_str for month in russian_months.keys()):
            russian_format_count += 1
            print("Russian format")
        else:
            other_format_count += 1
            print("Other format")
    
    # Summary
    total_dates = df['date'].notna().sum()
    print(f"\nFormat Analysis Summary:")
    print(f"Total dates found: {total_dates}")
    print(f"Sample analysis (first 10):")
    print(f"  - DD/MM/YYYY format: {dd_mm_yyyy_count}")
    print(f"  - Russian format: {russian_format_count}")
    print(f"  - Other formats: {other_format_count}")
    
    # Determine primary format
    if dd_mm_yyyy_count > russian_format_count:
        detected_format = "DD/MM/YYYY"
        needs_conversion = False
    else:
        detected_format = "Russian"
        needs_conversion = True
    
    print(f"\nDetected primary format: {detected_format}")
    print(f"Conversion needed: {'Yes' if needs_conversion else 'No'}")
    
    # Save analysis results for next script
    analysis_results = {
        'detected_format': detected_format,
        'needs_conversion': needs_conversion,
        'total_dates': total_dates,
        'sample_analysis': {
            'dd_mm_yyyy_count': dd_mm_yyyy_count,
            'russian_format_count': russian_format_count,
            'other_format_count': other_format_count
        }
    }
    
    with open('output/date_format_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    
    print(f"\nAnalysis results saved to: output/date_format_analysis.json")
    
else:
    print("No date column found!")

print(f"\nNext step: Run 3b_convert_dates.py to perform date conversion")
