# Student Performance Dataset

Cleaned and anonymized survey data from 12k+ students, enabling accurate academic trend analysis.

## Overview

This repository contains a comprehensive data cleaning pipeline for student survey responses exported from Google Forms. The pipeline transforms raw, unstructured survey data into analysis-ready datasets suitable for academic research and institutional decision-making.

### Dataset Characteristics
- **📊 Scale**: 12,000+ student responses
- **🎓 Scope**: Multi-departmental academic survey data
- **🔄 Processing**: Comprehensive cleaning and standardization
- **📈 Output**: Analysis-ready CSV and Excel formats

## Features

### Data Quality Assurance
- **Timestamp Validation**: Converts and validates temporal data with error handling
- **Identity Standardization**: Normalizes student ID formats for consistency
- **Age Validation**: Applies realistic constraints (18-60 years) with outlier removal
- **Category Standardization**: Corrects typos and standardizes demographic data

### Advanced Processing
- **Missing Value Imputation**: Linear interpolation for numerical data
- **Text Standardization**: Consistent comment formatting with spam detection
- **Grade Conversion**: Letter grades to numerical GPA (5.0 scale)
- **Department Expansion**: Abbreviation expansion to full department names

### Output Formats
- **CSV**: Universal compatibility for statistical software
- **Excel**: Formatted spreadsheet with descriptive sheet names
- **Comprehensive Logging**: Detailed processing statistics and validation metrics

## Quick Start

### Prerequisites
```bash
Python 3.8+
pandas >= 1.3.0
numpy >= 1.21.0
openpyxl >= 3.0.7
```

### Installation
```bash
# Clone the repository
git clone https://github.com/TADSTech/Student-survery-data-formatting.git
cd Student-survery-data-formatting

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Command Line
```bash
cd scripts
python cleanup.py
```

#### Jupyter Notebook
Open `notebooks/cleanup.ipynb` for interactive exploration and step-by-step analysis.

#### Programmatic Usage
```python
from scripts.cleanup import StudentDataCleaner

cleaner = StudentDataCleaner()
cleaned_df = cleaner.clean_dataset(
    input_path='data/raw/forms_responses_12955.csv',
    output_csv='data/cleaned/cleaned_student_data.csv',
    output_excel='data/cleaned/cleaned_student_data.xlsx'
)
```

## Data Pipeline

### Input Processing
1. **Raw Data Ingestion**: Google Forms CSV export
2. **Data Type Conversion**: Object to appropriate types (datetime, numeric, categorical)
3. **Missing Value Detection**: Comprehensive null value analysis

### Cleaning Operations
1. **Temporal Standardization**: Timestamp validation and formatting
2. **Identity Normalization**: Student ID consistency and format standardization
3. **Demographic Cleaning**: Gender and department category standardization
4. **Academic Metrics**: GPA conversion and satisfaction score validation
5. **Text Processing**: Comment standardization and spam filtering

### Quality Assurance
- Outlier detection and removal
- Data integrity validation
- Comprehensive logging and statistics
- Multi-format export with validation

## Project Structure

```
Student-survery-data-formatting/
├── data/
│   ├── raw/                    # Original survey data
│   │   └── forms_responses_12955.csv
│   └── cleaned/                # Processed datasets
│       ├── cleaned_student_data.csv
│       └── cleaned_student_data.xlsx
├── notebooks/
│   └── cleanup.ipynb          # Interactive analysis notebook
├── scripts/
│   └── cleanup.py             # Production cleaning pipeline
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation
```

## Data Schema

### Cleaned Dataset Columns
| Column | Type | Description |
|--------|------|-------------|
| `Timestamp` | datetime64[ns] | Survey submission timestamp |
| `Student_ID` | string | Normalized student identifier |
| `Age` | int | Validated age (18-60 years) |
| `Gender` | string | Standardized gender categories |
| `Department` | string | Full department names |
| `GPA` | float | Numeric GPA (1.0-5.0 scale) |
| `Satisfaction (1-5)` | float | Course satisfaction rating |
| `Comments` | string | Standardized feedback text |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/enhancement`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this dataset or cleaning pipeline in your research, please cite:

```bibtex
@dataset{student_performance_2025,
  title={Student Performance Dataset: Cleaned Survey Data},
  author={TADS Tech},
  year={2025},
  publisher={GitHub},
  url={https://github.com/TADSTech/Student-survery-data-formatting}
}
```

---

**📧 Contact**: For questions or collaboration opportunities, please open an issue or contact the maintainers.

**🔗 Links**: [GitHub Repository](https://github.com/TADSTech/Student-survery-data-formatting)