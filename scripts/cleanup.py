import pandas as pd
import numpy as np
import os

def clean_student_data(input_csv, output_csv, output_excel):
    # Load data
    std = pd.read_csv(input_csv)

    # Timestamp column
    std['Timestamp'] = pd.to_datetime(std['Timestamp'], errors='coerce')
    std.dropna(subset=['Timestamp'], inplace=True)

    # Student ID column
    std.rename(columns={'Student ID': 'Student_ID'}, inplace=True)
    std['Student_ID'] = std['Student_ID'].str.lower().str.strip()

    # Age column
    std['Age'] = pd.to_numeric(std['Age'], errors='coerce')
    std.dropna(subset=['Age'], inplace=True)
    std = std[(std['Age'] >= 18) & (std['Age'] <= 60)]
    std['Age'] = std['Age'].astype(int)

    # Gender column
    std['Gender'] = std['Gender'].replace({
        'Femal': 'Female',
        'Malee': 'Male',
        'Othr': 'Other',
        np.nan: 'Other'
    })
    std['Gender'] = std['Gender'].fillna('Other')
    std['Gender'] = std['Gender'].str.title()
    std['Gender'] = std['Gender'].astype('string')

    # Department column
    std['Department'] = std['Department'].replace({
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
    })
    std['Department'] = std['Department'].fillna('Undeclared')
    std['Department'] = std['Department'].astype('string')

    # GPA column
    std['GPA'] = std['GPA'].replace({
        'A': 4.5,
        'B': 3.5,
        'C': 3.0,
        'D': 2.5,
        'F': 1.5
    })
    std['GPA'] = pd.to_numeric(std['GPA'], errors='coerce')
    std['GPA'] = std['GPA'].fillna(std['GPA'].interpolate(method='linear'))
    std['GPA'] = std['GPA'].round(2)
    std = std[std['GPA'] >= 1.0]

    # Satisfaction column
    std['Satisfaction (1-5)'] = std['Satisfaction (1-5)'].fillna(
        std['Satisfaction (1-5)'].interpolate(method='linear')
    )
    std['Satisfaction (1-5)'] = std['Satisfaction (1-5)'].round(2)
    std = std[std['Satisfaction (1-5)'] >= 1.0]

    # Comments column
    std['Comments'] = std['Comments'].fillna("The course was great!")
    std = std.sort_values('Timestamp', ascending=True).reset_index(drop=True)

    def comments_standardize(idx, text):
        if isinstance(text, str) and text.startswith('This is spam'):
            return f'Comment {idx}: The course was great!'
        elif isinstance(text, str) and text.startswith('Comment'):
            parts = text.split(':', 1)
            if len(parts) > 1:
                return f'Comment {idx}: {parts[1].strip()}'
            return f'Comment {idx}: No comment'
        elif isinstance(text, str) and text.strip():
            return f'Comment {idx}: {text.strip()}'
        else:
            return f'Comment {idx}: No comment'

    std['Comments'] = [comments_standardize(i, txt) for i, txt in enumerate(std['Comments'])]
    std['Comments'] = std['Comments'].astype('string')

    # Save cleaned data
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    std.to_csv(output_csv, index=False)
    std.to_excel(output_excel, index=False, sheet_name='Cleaned Student Data')

if __name__ == "__main__":
    input_csv = os.path.join('..', 'data', 'raw', 'forms_responses_12955.csv')
    output_csv = os.path.join('..', 'data', 'cleaned', 'cleaned_student_data.csv')
    output_excel = os.path.join('..', 'data', 'cleaned', 'cleaned_student_data.xlsx')
    clean_student_data(input_csv, output_csv, output_excel)