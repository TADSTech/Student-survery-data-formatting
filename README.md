# Student Survey Data Cleaning

This project cleans and standardizes student survey data exported from Google Forms.

## Features

- Cleans timestamp, student ID, age, gender, department, GPA, satisfaction, and comments columns
- Handles typos, missing values, and outliers
- Outputs cleaned data as CSV and Excel files

## Usage

1. Place your raw CSV file in `data/raw/` (default: `forms_responses_12955.csv`).
2. Run the script:

   ```sh
   cd src
   python cleanup.py
   ```

3. Cleaned files will be saved in `data/cleaned/`.

## Requirements

- Python 3.8+
- pandas
- numpy
- openpyxl (for Excel output)

Install dependencies with:

```sh
pip install requirements.txt
```

## Customization

Edit `scripts/cleanup.py` to change file paths or cleaning logic as needed.