"""
Student Performance Dataset - Data Cleaning Pipeline
===================================================

This module provides comprehensive data cleaning and standardization for student survey
responses exported from Google Forms. The pipeline handles missing values, outliers,
data type conversions, and text standardization to produce analysis-ready datasets.

Author: TADS Tech
Date: October 2025
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import logging
from typing import Tuple, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StudentDataCleaner:
    """
    A comprehensive data cleaning pipeline for student survey responses.
    
    This class provides methods to clean, validate, and standardize student
    survey data with robust error handling and detailed logging.
    """
    
    def __init__(self):
        """Initialize the data cleaner with predefined mappings."""
        self.gender_mapping = {
            'Femal': 'Female',
            'Malee': 'Male',
            'Othr': 'Other',
            np.nan: 'Other'
        }
        
        self.department_mapping = {
            np.nan: 'Undeclared',
            'Marine Sci': 'Marine Sciences',
            'Geo': 'Geosciences',
            'Biochem': 'Biochemistry',
            'Maths': 'Mathematics',
            'Phys': 'Physics',
            'Bio': 'Biology',
            'Cell Bio': 'Cell Biology and Genetics',
            'Chem': 'Chemistry',
            'Geophy': 'Geophysics',
            'Zoo': 'Zoology',
            'Microbio': 'Microbiology',
            'Comp Sci': 'Computer Science'
        }
        
        self.grade_mapping = {
            'A': 4.5, 'B': 3.5, 'C': 3.0, 'D': 2.5, 'F': 1.5
        }
    
    def _clean_timestamps(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate timestamp data."""
        logger.info("Processing timestamps...")
        original_count = len(df)
        
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df.dropna(subset=['Timestamp'], inplace=True)
        
        removed_count = original_count - len(df)
        logger.info(f"Timestamp cleaning: {removed_count} invalid records removed")
        return df
    
    def _clean_student_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize student ID format."""
        logger.info("Standardizing student IDs...")
        
        df.rename(columns={'Student ID': 'Student_ID'}, inplace=True)
        df['Student_ID'] = df['Student_ID'].str.lower().str.strip()
        
        logger.info(f"Student IDs processed: {df['Student_ID'].nunique()} unique IDs")
        return df
    
    def _clean_ages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean age data."""
        logger.info("Processing age data...")
        original_count = len(df)
        
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        df.dropna(subset=['Age'], inplace=True)
        df = df[(df['Age'] >= 18) & (df['Age'] <= 60)]
        df['Age'] = df['Age'].astype(int)
        
        removed_count = original_count - len(df)
        logger.info(f"Age validation: {removed_count} records removed (invalid/out-of-range)")
        return df
    
    def _clean_gender(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize gender categories."""
        logger.info("Standardizing gender data...")
        
        df['Gender'] = df['Gender'].replace(self.gender_mapping)
        df['Gender'] = df['Gender'].fillna('Other').str.title().astype('string')
        
        logger.info(f"Gender distribution: {dict(df['Gender'].value_counts())}")
        return df
    
    def _clean_departments(self, df: pd.DataFrame) -> pd.DataFrame:
        """Expand and standardize department names."""
        logger.info("Standardizing department names...")
        
        df['Department'] = df['Department'].replace(self.department_mapping)
        df['Department'] = df['Department'].fillna('Undeclared').astype('string')
        
        logger.info(f"Departments processed: {df['Department'].nunique()} unique departments")
        return df
    
    def _clean_gpa(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert and validate GPA data."""
        logger.info("Processing GPA data...")
        original_count = len(df)
        
        df['GPA'] = df['GPA'].replace(self.grade_mapping)
        df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
        
        # Impute missing values
        missing_count = df['GPA'].isna().sum()
        df['GPA'] = df['GPA'].fillna(df['GPA'].interpolate(method='linear'))
        df['GPA'] = df['GPA'].round(2)
        
        # Remove outliers
        df = df[df['GPA'] >= 1.0]
        
        removed_count = original_count - len(df)
        logger.info(f"GPA processing: {missing_count} values imputed, {removed_count} outliers removed")
        return df
    
    def _clean_satisfaction(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate satisfaction scores."""
        logger.info("Processing satisfaction scores...")
        original_count = len(df)
        
        missing_count = df['Satisfaction (1-5)'].isna().sum()
        df['Satisfaction (1-5)'] = df['Satisfaction (1-5)'].fillna(
            df['Satisfaction (1-5)'].interpolate(method='linear')
        )
        df['Satisfaction (1-5)'] = df['Satisfaction (1-5)'].round(2)
        df = df[df['Satisfaction (1-5)'] >= 1.0]
        
        removed_count = original_count - len(df)
        logger.info(f"Satisfaction processing: {missing_count} values imputed, {removed_count} outliers removed")
        return df
    
    def _standardize_comment(self, idx: int, text: str) -> str:
        """Standardize individual comment format."""
        if isinstance(text, str) and text.startswith('This is spam'):
            return f'Comment {idx}: The course was great!'
        elif isinstance(text, str) and text.startswith('Comment'):
            parts = text.split(':', 1)
            content = parts[1].strip() if len(parts) > 1 else 'No comment'
            return f'Comment {idx}: {content}'
        elif isinstance(text, str) and text.strip():
            return f'Comment {idx}: {text.strip()}'
        else:
            return f'Comment {idx}: No comment'
    
    def _clean_comments(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize comment format and handle spam."""
        logger.info("Standardizing comments...")
        
        df['Comments'] = df['Comments'].fillna("The course was great!")
        df = df.sort_values('Timestamp', ascending=True).reset_index(drop=True)
        
        df['Comments'] = [
            self._standardize_comment(i, txt) 
            for i, txt in enumerate(df['Comments'])
        ]
        df['Comments'] = df['Comments'].astype('string')
        
        logger.info(f"Comments standardized: {len(df)} comments processed")
        return df
    
    def clean_dataset(self, input_path: str, output_csv: str, output_excel: str) -> pd.DataFrame:
        """
        Execute the complete data cleaning pipeline.
        
        Args:
            input_path: Path to the raw CSV file
            output_csv: Path for cleaned CSV output
            output_excel: Path for cleaned Excel output
            
        Returns:
            Cleaned pandas DataFrame
        """
        try:
            logger.info(f"Starting data cleaning pipeline for: {input_path}")
            
            # Load data
            df = pd.read_csv(input_path)
            logger.info(f"Dataset loaded: {len(df):,} records, {len(df.columns)} columns")
            
            # Apply cleaning pipeline
            df = self._clean_timestamps(df)
            df = self._clean_student_ids(df)
            df = self._clean_ages(df)
            df = self._clean_gender(df)
            df = self._clean_departments(df)
            df = self._clean_gpa(df)
            df = self._clean_satisfaction(df)
            df = self._clean_comments(df)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_csv), exist_ok=True)
            
            # Export cleaned data
            df.to_csv(output_csv, index=False)
            df.to_excel(output_excel, index=False, sheet_name='Cleaned Student Data')
            
            # Log final statistics
            logger.info("="*60)
            logger.info("DATA CLEANING PIPELINE COMPLETE")
            logger.info("="*60)
            logger.info(f"Final dataset: {len(df):,} records")
            logger.info(f"Date range: {df['Timestamp'].min().date()} to {df['Timestamp'].max().date()}")
            logger.info(f"Age range: {df['Age'].min()}-{df['Age'].max()} years")
            logger.info(f"Average GPA: {df['GPA'].mean():.2f}")
            logger.info(f"Average satisfaction: {df['Satisfaction (1-5)'].mean():.2f}")
            logger.info(f"Files saved: {output_csv}, {output_excel}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error in data cleaning pipeline: {str(e)}")
            raise


def clean_student_data(input_csv: str, output_csv: str, output_excel: str) -> pd.DataFrame:
    """
    Main function to clean student survey data.
    
    Args:
        input_csv: Path to raw CSV file
        output_csv: Path for cleaned CSV output  
        output_excel: Path for cleaned Excel output
        
    Returns:
        Cleaned pandas DataFrame
    """
    cleaner = StudentDataCleaner()
    return cleaner.clean_dataset(input_csv, output_csv, output_excel)

if __name__ == "__main__":
    # Define file paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    input_csv = project_root / 'data' / 'raw' / 'forms_responses_12955.csv'
    output_csv = project_root / 'data' / 'cleaned' / 'cleaned_student_data.csv'
    output_excel = project_root / 'data' / 'cleaned' / 'cleaned_student_data.xlsx'
    
    # Execute cleaning pipeline
    try:
        cleaned_df = clean_student_data(
            str(input_csv), 
            str(output_csv), 
            str(output_excel)
        )
        print("\n🚀 Data cleaning completed successfully!")
        print(f"📊 Final dataset: {len(cleaned_df):,} records ready for analysis")
        
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at {input_csv}")
        print("Please ensure the raw data file exists in the data/raw/ directory.")
        
    except Exception as e:
        print(f"❌ Error during data cleaning: {str(e)}")
        print("Please check the input data format and try again.")