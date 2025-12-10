# LinkedIn Jobs Data Processing - Saudi Arabia 2020

A comprehensive text processing pipeline for analyzing LinkedIn job postings in Saudi Arabia from 2020.

## 📊 Dataset Overview

- **Source**: LinkedIn Job Posts in Saudi Arabia 2020
- **Original Records**: 48,449 job entries
- **Processed Records**: ~41,000 jobs (after cleaning)
- **Time Period**: 2020

## 🚀 Features

### Data Processing
- **Location Standardization**: Maps cities to Saudi regions
- **Industry Categorization**: Extracts and standardizes industry types
- **Date Components**: Extracts day, month, quarter from posting dates
- **Text Cleaning**: Removes special characters and common phrases

### Advanced Extraction
- **Years of Experience**: Extracts experience requirements from job descriptions
- **Education Degrees**: Identifies required education levels (Bachelor, Master, PhD, etc.)
- **Salary Information**: Detects salary mentions in job postings
- **Skills Detection**: Identifies technical skills (Python, Java, SQL, etc.)

### Data Quality
- **Corrupt Row Removal**: Filters out jobs with insufficient descriptions
- **Null Value Handling**: Smart imputation based on job levels
- **Text Normalization**: Standardizes text format and encoding

## 📁 Project Structure

```
├── text_processing.py          # Main processing script
├── data_jobs.csv              # Processed output data
├── Linkedin Job Posts in Saudi Arabia 2020.xlsx  # Original dataset
└── README.md                  # This file
```

## 🛠️ Requirements

```python
pandas
numpy
seaborn
matplotlib
openpyxl
re
warnings
```

## 📈 Key Insights

### Top Job Markets
1. **Riyadh**: 22,380+ jobs (51.2%)
2. **Remote**: 8,949+ jobs (20.5%)
3. **Makkah**: 6,033+ jobs (13.8%)
4. **Eastern Province**: 3,813+ jobs (8.7%)

### Top Industries
1. **Information Technology**: 6,554+ jobs
2. **Construction**: 3,937+ jobs
3. **Marketing & Advertising**: 2,036+ jobs
4. **Computer**: 2,007+ jobs

## 🔧 Usage

1. **Install Requirements**:
   ```bash
   pip install pandas numpy seaborn matplotlib openpyxl
   ```

2. **Run Processing**:
   ```bash
   python text_processing.py
   ```

3. **Output**: 
   - `data_jobs.csv` - Cleaned and processed dataset

## 📋 Output Columns

| Column | Description |
|--------|-------------|
| `position` | Job title |
| `company` | Company name |
| `level` | Job level (Entry, Mid, Senior, etc.) |
| `city` | Standardized city name |
| `Regions` | Saudi Arabia regions |
| `industry_cat` | Industry category |
| `year_of_ex` | Required years of experience |
| `salary_mentioned` | Salary information (if mentioned) |
| `skills` | Detected technical skills |
| `description_length` | Job description word count |
| `is_remote` | Remote job indicator (0/1) |
| `day`, `month`, `quarter` | Date components |

## 🎯 Data Quality Metrics

- **Text Processing**: Removes 2,453+ short/corrupt job descriptions
- **Industry Filtering**: Processes 43,679+ jobs with valid industry data
- **Experience Extraction**: Identifies experience requirements in 29,000+ jobs
- **Skills Detection**: Finds technical skills in 12,000+ job descriptions
- **Salary Information**: Detects salary mentions in relevant postings

## 🔍 Processing Pipeline

1. **Data Loading**: Load Excel file with job postings
2. **Location Processing**: Clean and standardize city/region names
3. **Industry Extraction**: Categorize jobs by industry type
4. **Text Cleaning**: Remove special characters and common phrases
5. **Feature Extraction**: Extract experience, education, skills, salary
6. **Quality Control**: Remove corrupt/incomplete records
7. **Export**: Save processed data to CSV

## 📊 Sample Analysis

```python
import pandas as pd

# Load processed data
df = pd.read_csv('data_jobs.csv')

# Top regions by job count
print(df['Regions'].value_counts().head())

# Average experience by industry
print(df.groupby('industry_cat')['year_of_ex'].mean().head())

# Remote vs on-site jobs
print(f"Remote jobs: {df['is_remote'].sum():,}")
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Abdullah Aldeijy**
- GitHub: [@AbdullahAldeijy](https://github.com/AbdullahAldeijy)

---

*This project provides comprehensive text processing and analysis capabilities for LinkedIn job market data in Saudi Arabia.*