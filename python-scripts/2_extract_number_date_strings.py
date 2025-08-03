import pandas as pd
import json
import re

# Load the recently saved JSON file
with open('../output/01_title_description_cleaned.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Display basic info about the loaded data
print("Loaded DataFrame shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
print(df[['title']].head())

# Extract lecture information using regex pattern
# Pattern: "Лекцию №*Сергей Бугаев прочитал*года"
# We want to extract: 
# 1. Text between "№" and "Сергей" 
# 2. Text between "прочитал" and "года"

def extract_lecture_info(description):
    if pd.isna(description):
        return None, None
    
    # Pattern 1: "© Лекцию №X (часть Y) Сергей Бугаев прочитал DATE года"
    pattern1 = r'©\s*Лекцию\s+№\s*([^(]*?)\s*\(часть\s*([^)]*?)\)\s*Сергей\s+Бугаев\s+прочитал\s+(.*?)\s+года'
    match1 = re.search(pattern1, description, re.IGNORECASE | re.DOTALL)
    
    if match1:
        lecture_number = match1.group(1).strip()
        part_number = match1.group(2).strip()
        lecture_date = match1.group(3).strip()
        # Combine lecture number and part number in X-Y format
        combined_number = f"{lecture_number}-{part_number}"
        return combined_number, lecture_date
    
    # Pattern 2: "© Лекцию №X Сергей Бугаев прочитал DATE года" (without части)
    pattern2 = r'©\s*Лекцию\s+№\s*([^С]*?)\s*Сергей\s+Бугаев\s+прочитал\s+(.*?)\s+года'
    match2 = re.search(pattern2, description, re.IGNORECASE | re.DOTALL)
    
    if match2:
        lecture_number = match2.group(1).strip()
        lecture_date = match2.group(2).strip()
        return lecture_number, lecture_date
    
    # Pattern 3: "Лекция прочитана DATE года" (no number, just date)
    pattern3 = r'Лекция\s+прочитана\s+(.*?)\s+года'
    match3 = re.search(pattern3, description, re.IGNORECASE | re.DOTALL)
    
    if match3:
        lecture_number = None
        lecture_date = match3.group(1).strip()
        return lecture_number, lecture_date
    
    return None, None

# Apply the extraction function to each row
print("\nExtracting lecture information...")
lecture_info = df['description'].apply(extract_lecture_info)

# Create new columns for the extracted information
df['number'] = [info[0] for info in lecture_info]
df['date'] = [info[1] for info in lecture_info]

# Display results
print("\nExtraction results:")
print("="*50)
for idx, row in df.iterrows():
    print(f"Title: {row['title']}")
    print(f"Number: {row['number']}")
    print(f"Date: {row['date']}")
    print("-" * 30)

# Show only rows where extraction was successful
extracted_df = df[df['number'].notna()]
print(f"\nFound {len(extracted_df)} rows with lecture information:")
print(extracted_df[['title', 'number', 'date']])

# Save the enhanced DataFrame with extracted information
output_file = '../output/02_lectures_with_extracted_info.json'
df_records = df.to_dict(orient='records')

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(df_records, json_file, ensure_ascii=False, indent=4)

print(f"\nEnhanced data saved to: {output_file}")

# Optional: Save as CSV for easier viewing with proper UTF-8 BOM and semicolon delimiter
df.to_csv('../output/02_lectures_with_extracted_info.csv', index=False, encoding='utf-8-sig', sep=';')
print("Also saved as CSV: ../output/02_lectures_with_extracted_info.csv")