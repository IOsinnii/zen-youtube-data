import pandas as pd
import json

# Load the prepared data
with open('output/lectures_prepared_for_sorting.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

print("Loaded DataFrame shape:", df.shape)
print("Columns:", df.columns.tolist())

# Perform multi-level sorting
print("\nSorting lectures chronologically...")
print("Sort order: 1) Date (earliest first), 2) Lecture number, 3) Part number")

df_sorted = df.sort_values(['date_datetime', 'lecture_num', 'part_num'], 
                          ascending=[True, True, True]).reset_index(drop=True)

# Create order column
df_sorted['order'] = range(1, len(df_sorted) + 1)

print(f"\nSorting complete! Created order from 1 to {len(df_sorted)}")

# Show first 10 ordered results
print(f"\nFirst 10 lectures in chronological order:")
print("="*70)
for idx, row in df_sorted.head(10).iterrows():
    date_display = row.get('date_standard', row.get('date', 'N/A'))
    print(f"Order: {row['order']}")
    print(f"Title: {row['title']}")
    print(f"Number: {row['number']} (Lecture: {row['lecture_num']}, Part: {row['part_num']})")
    print(f"Date: {date_display}")
    print("-" * 50)

# Clean up temporary columns for final export
print(f"\nPreparing final export...")
columns_to_drop = ['date_datetime', 'lecture_num', 'part_num']

# Handle missing values
if 'date_standard' in df_sorted.columns:
    df_sorted['date_standard'] = df_sorted['date_standard'].fillna('')

if 'date' in df_sorted.columns:
    df_sorted['date'] = df_sorted['date'].fillna('').astype(str)

# Create final DataFrame
df_final = df_sorted.drop(columns=[col for col in columns_to_drop if col in df_sorted.columns], errors='ignore')

# Reorder columns for better readability
available_columns = df_final.columns.tolist()
preferred_order = ['order', 'title', 'number', 'date', 'date_standard', 'description']
remaining_columns = [col for col in available_columns if col not in preferred_order]
column_order = [col for col in preferred_order if col in available_columns] + remaining_columns
df_final = df_final[column_order]

print(f"Final columns: {df_final.columns.tolist()}")

# Save final results
output_json = 'output/lectures_with_order.json'
df_records = df_final.to_dict(orient='records')

with open(output_json, 'w', encoding='utf-8') as json_file:
    json.dump(df_records, json_file, ensure_ascii=False, indent=4)

print(f"\nFinal data saved to: {output_json}")

# Save Excel format
output_excel = 'output/lectures_with_order.xlsx'
df_final.to_excel(output_excel, index=False, engine='openpyxl')
print(f"Also saved to Excel: {output_excel}")

# Display summary statistics
print(f"\nFinal Summary:")
print(f"Total lectures: {len(df_final)}")
print(f"Lectures with numbers: {df_final['number'].notna().sum()}")
print(f"Lectures without numbers: {df_final['number'].isna().sum()}")

# Date range
try:
    valid_dates = df_final['date'].dropna()
    if len(valid_dates) > 0:
        valid_dates = valid_dates.astype(str)
        print(f"Date range: {valid_dates.min()} to {valid_dates.max()}")
    else:
        print("Date range: No valid dates found")
except Exception as e:
    print(f"Date range: Error calculating - {e}")

print(f"\nChronological ordering complete!")
print(f"Files created:")
print(f"- {output_json}")
print(f"- {output_excel}")
