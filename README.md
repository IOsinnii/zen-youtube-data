# YouTube Lecture Data Processing Pipeline

A comprehensive Python-based data processing pipeline for cleaning and organizing YouTube lecture data for web catalogue database integration.

## Project Purpose

This project transforms raw YouTube scraper data into a clean, structured dataset suitable for building a web catalogue of lectures. The pipeline handles:

- **Date standardization**: Converting Russian dates and mixed formats to machine-readable DD/MM/YYYY format
- **Lecture numbering**: Extracting and parsing lecture numbers from Russian text descriptions
- **Data cleaning**: Removing unnecessary columns and standardizing text content
- **Chronological ordering**: Creating sequential order for filtering and sorting in web applications

## Project Structure

```
zen-youtube-data/
├── input/                           # Source data files
│   ├── dataset_youtube-scraper-task_2025-04-26.json
│   └── dataset_youtube-scraper-task_2025-04-26_subset.json
├── output/                          # Processed data files
│   ├── 01_title_description_cleaned.csv
│   ├── 02_lectures_with_extracted_info.json
│   ├── 03b_lectures_with_reformatted_dates.json
│   ├── 4a_lectures_prepared_for_sorting.json
│   └── 4b_lectures_with_order.json
├── python-scripts/                  # Processing pipeline scripts
│   ├── 1_extract_rename_columns.py
│   ├── 2_extract_number_date_strings.py
│   ├── 3a_analyze_date_format.py
│   ├── 3b_convert_dates.py
│   ├── 3c_merge_3b_output_and_pub_date.py
│   ├── 4a_prepare_sorting.py
│   └── 4b_create_chronological_order.py
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project configuration
└── README.md                        # This documentation
```

## Data Processing Pipeline

### Overview
The pipeline processes YouTube lecture data through 4 main stages:

```
Raw JSON Data → Data Cleaning → Information Extraction → Date Processing → Chronological Ordering
```

### Stage 1: Data Cleaning (`1_extract_rename_columns.py`)
**Purpose**: Clean and standardize the initial dataset
- Removes unnecessary columns (`order`, `thumbnailUrl`, `date`, `id`, `url`, `duration`)
- Renames `text` field to `description` for clarity
- Exports clean data in both CSV and JSON formats

**Input**: `input/dataset_youtube-scraper-task_2025-04-26.json`
**Output**: `output/01_title_description_cleaned.json`

### Stage 2: Information Extraction (`2_extract_number_date_strings.py`)
**Purpose**: Extract lecture numbers and dates from Russian text descriptions
- Uses regex patterns to identify lecture numbering formats:
  - `© Лекцию №126 (часть 2) Сергей Бугаев прочитал 16 мая 2021 года` (multi-part)
  - `© Лекцию №126 Сергей Бугаев прочитал 16 мая 2021 года` (single)
  - `Лекция прочитана 16 мая 2021 года` (date only)
- Extracts structured data: lecture number, part number, and date

**Input**: `output/01_title_description_cleaned.json`
**Output**: `output/02_lectures_with_extracted_info.json`

### Stage 3: Date Processing
#### 3a. Date Format Analysis (`3a_analyze_date_format.py`)
**Purpose**: Analyze and detect date formats in the dataset
- Identifies Russian vs DD/MM/YYYY formats
- Provides conversion statistics and recommendations
- Saves analysis results for the conversion step

**Output**: `output/03b_date_format_analysis.json`

#### 3b. Date Conversion (`3b_convert_dates.py`)
**Purpose**: Convert dates to standardized DD/MM/YYYY format
- Handles Russian month names (`января`, `февраля`, etc.)
- Preserves existing DD/MM/YYYY dates
- Creates `date_standard` column with machine-readable dates
- Provides detailed conversion reporting

**Input**: `output/02_lectures_with_extracted_info.json`
**Output**: `output/03b_lectures_with_reformatted_dates.json`

### Stage 4: Chronological Ordering
#### 4a. Sorting Preparation (`4a_prepare_sorting.py`)
**Purpose**: Prepare data for chronological sorting
- Extracts numeric lecture and part numbers for sorting
- Converts dates to datetime objects
- Creates sorting keys while preserving original data

**Input**: `output/03b_lectures_with_reformatted_dates.json`
**Output**: `output/4a_lectures_prepared_for_sorting.json`

#### 4b. Final Ordering (`4b_create_chronological_order.py`)
**Purpose**: Create final chronologically ordered dataset
- Multi-level sorting: Date → Lecture Number → Part Number
- Assigns sequential `order` field (1, 2, 3, ...)
- Exports final dataset in JSON and Excel formats

**Input**: `output/4a_lectures_prepared_for_sorting.json`
**Output**: 
- `output/4b_lectures_with_order.json`
- `output/4b_lectures_with_order.xlsx`

## Installation & Setup

### Prerequisites
- Python 3.11+
- `uv` package manager (recommended) or `pip`

### Using uv (Recommended)
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt
```

### Using pip
```bash
pip install -r requirements.txt
```

## Usage

### Running the Complete Pipeline
Execute scripts in sequence from the `python-scripts/` directory:

```bash
cd python-scripts

# Stage 1: Clean data
python 1_extract_rename_columns.py

# Stage 2: Extract information
python 2_extract_number_date_strings.py

# Stage 3: Process dates
python 3a_analyze_date_format.py
python 3b_convert_dates.py

# Stage 4: Create chronological order
python 4a_prepare_sorting.py
python 4b_create_chronological_order.py
```

### Running Individual Stages
Each script can be run independently if you have the required input files:

```bash
# Just convert dates (requires stage 2 output)
python 3b_convert_dates.py

# Just create final ordering (requires stage 3 output)
python 4a_prepare_sorting.py
python 4b_create_chronological_order.py
```

## Output Data Structure

### Final Dataset Schema
The final output (`4b_lectures_with_order.json`) contains:

```json
{
  "order": 1,                    // Sequential order for web catalogue
  "title": "Лекция о...",        // Original lecture title
  "number": "126-2",             // Extracted lecture number
  "date": "16 мая 2021 года",    // Original date string
  "date_standard": "16/05/2021", // Machine-readable date
  "description": "© Лекцию..."   // Full description text
}
```

### Key Fields for Web Catalogue
- **`order`**: Sequential numbering for default sorting
- **`date_standard`**: Standardized dates for filtering by time periods
- **`number`**: Lecture numbers for academic sequence navigation
- **`title`**: Display titles for the catalogue interface
- **`description`**: Full content for search functionality

## Data Quality & Statistics

### Processing Results
- **Total lectures processed**: 219
- **Lectures with extracted numbers**: ~138 (63%)
- **Date conversion success rate**: ~95%
- **Output formats**: JSON (machine-readable) + Excel (human-readable)

### Data Cleaning Achievements
- ✅ Standardized date formats for database storage
- ✅ Extracted structured lecture numbering
- ✅ Preserved original data for reference
- ✅ Created sortable chronological order
- ✅ UTF-8 encoding for Cyrillic text support

## Integration with Web Catalogue

### Database Schema Recommendations
```sql
CREATE TABLE lectures (
    id SERIAL PRIMARY KEY,
    order_num INTEGER,           -- From 'order' field
    title TEXT,                  -- From 'title' field  
    lecture_number VARCHAR(20),  -- From 'number' field
    lecture_date DATE,           -- From 'date_standard' field
    description TEXT,            -- From 'description' field
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API Endpoints
The processed data supports common catalogue operations:
- **List all lectures**: `GET /lectures?order_by=order`
- **Filter by date range**: `GET /lectures?date_from=2021-01-01&date_to=2021-12-31`
- **Search by title**: `GET /lectures?search=keyword`
- **Get by lecture number**: `GET /lectures?number=126`

### Frontend Integration
- Use `order` field for default chronological listing
- Use `date_standard` for date-based filtering widgets
- Use `number` field for lecture sequence navigation
- Use `title` and `description` for search functionality

## Development & Maintenance

### Adding New Data
To process additional YouTube data:
1. Place new JSON files in `input/` directory
2. Update file paths in script 1
3. Run the complete pipeline
4. Merge results with existing database

### Customizing the Pipeline
- **Date formats**: Modify `russian_months` dictionary in stage 3
- **Extraction patterns**: Update regex patterns in stage 2
- **Output schema**: Adjust column selection in stage 4
- **Sorting logic**: Modify sort keys in stage 4b

### Quality Assurance
Each stage includes validation and reporting:
- Extraction success rates
- Date conversion statistics  
- Data integrity checks
- Sample output verification

## License

This project is developed for academic/research purposes. Please ensure compliance with YouTube's Terms of Service when processing scraped data.

---

**Last Updated**: August 2025  
**Pipeline Version**: 2.0  
**Supported Data Formats**: JSON, CSV, Excel
