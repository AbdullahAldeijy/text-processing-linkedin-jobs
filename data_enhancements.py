# Data Enhancement Functions for LinkedIn Jobs Dataset
import pandas as pd
import numpy as np
import re
from datetime import datetime

def extract_job_type(description):
    """Extract job type (full-time, part-time, contract, internship)"""
    if pd.isna(description):
        return np.nan
    
    description = description.lower()
    if any(word in description for word in ['full time', 'full-time', 'permanent']):
        return 'Full-time'
    elif any(word in description for word in ['part time', 'part-time']):
        return 'Part-time'
    elif any(word in description for word in ['contract', 'contractor', 'freelance']):
        return 'Contract'
    elif any(word in description for word in ['intern', 'internship', 'trainee']):
        return 'Internship'
    else:
        return 'Not Specified'

def extract_company_size(description):
    """Extract company size indicators"""
    if pd.isna(description):
        return np.nan
    
    description = description.lower()
    if any(word in description for word in ['startup', 'small company', 'growing team']):
        return 'Small'
    elif any(word in description for word in ['medium', 'established', '100+ employees']):
        return 'Medium'
    elif any(word in description for word in ['large', 'multinational', 'global', 'fortune', '1000+ employees']):
        return 'Large'
    else:
        return 'Unknown'

def extract_benefits(description):
    """Extract job benefits mentioned"""
    if pd.isna(description):
        return np.nan
    
    benefits = []
    description = description.lower()
    
    benefit_keywords = {
        'health_insurance': ['health insurance', 'medical', 'healthcare'],
        'housing_allowance': ['housing', 'accommodation', 'housing allowance'],
        'transportation': ['transportation', 'transport', 'car allowance'],
        'training': ['training', 'development', 'courses', 'certification'],
        'vacation': ['vacation', 'annual leave', 'paid leave'],
        'bonus': ['bonus', 'incentive', 'commission']
    }
    
    for benefit, keywords in benefit_keywords.items():
        if any(keyword in description for keyword in keywords):
            benefits.append(benefit)
    
    return ', '.join(benefits) if benefits else np.nan

def categorize_seniority(level, years_exp):
    """Categorize job seniority based on level and experience"""
    if pd.isna(level):
        level = ''
    
    level = str(level).lower()
    
    if any(word in level for word in ['entry', 'junior', 'intern', 'graduate']):
        return 'Entry Level'
    elif any(word in level for word in ['senior', 'lead', 'principal']):
        return 'Senior Level'
    elif any(word in level for word in ['manager', 'director', 'head', 'chief']):
        return 'Management'
    elif years_exp <= 2:
        return 'Entry Level'
    elif years_exp <= 5:
        return 'Mid Level'
    elif years_exp > 5:
        return 'Senior Level'
    else:
        return 'Mid Level'

def extract_work_model(description, regions):
    """Extract work model (remote, hybrid, on-site)"""
    if 'Remote' in str(regions):
        return 'Remote'
    
    if pd.isna(description):
        return 'On-site'
    
    description = description.lower()
    if any(word in description for word in ['remote', 'work from home', 'wfh']):
        return 'Remote'
    elif any(word in description for word in ['hybrid', 'flexible']):
        return 'Hybrid'
    else:
        return 'On-site'

def extract_language_requirements(description):
    """Extract language requirements"""
    if pd.isna(description):
        return np.nan
    
    languages = []
    description = description.lower()
    
    language_patterns = {
        'arabic': ['arabic', 'عربي'],
        'english': ['english', 'fluent english'],
        'french': ['french'],
        'german': ['german'],
        'spanish': ['spanish']
    }
    
    for lang, patterns in language_patterns.items():
        if any(pattern in description for pattern in patterns):
            languages.append(lang)
    
    return ', '.join(languages) if languages else np.nan

def calculate_job_attractiveness_score(row):
    """Calculate job attractiveness score based on multiple factors"""
    score = 0
    
    # Salary mentioned (+2)
    if pd.notna(row.get('salary_mentioned')):
        score += 2
    
    # Skills mentioned (+1)
    if pd.notna(row.get('skills')):
        score += 1
    
    # Benefits mentioned (+1)
    if pd.notna(row.get('benefits')):
        score += 1
    
    # Remote work (+1)
    if row.get('work_model') == 'Remote':
        score += 1
    
    # Description length (longer = more detailed = +1)
    if row.get('description_length', 0) > 500:
        score += 1
    
    return score

def enhance_dataset(df):
    """Apply all enhancement functions to the dataset"""
    print("Enhancing dataset with additional features...")
    
    # Apply enhancement functions
    df['job_type'] = df['description'].apply(extract_job_type)
    df['company_size'] = df['description'].apply(extract_company_size)
    df['benefits'] = df['description'].apply(extract_benefits)
    df['seniority_level'] = df.apply(lambda x: categorize_seniority(x['level'], x.get('year_of_ex', 0)), axis=1)
    df['work_model'] = df.apply(lambda x: extract_work_model(x['description'], x['Regions']), axis=1)
    df['language_requirements'] = df['description'].apply(extract_language_requirements)
    df['job_attractiveness_score'] = df.apply(calculate_job_attractiveness_score, axis=1)
    
    print("Enhancement completed!")
    return df

# Usage example:
if __name__ == "__main__":
    # Load your processed data
    df = pd.read_csv('data_jobs.csv')
    
    # Enhance the dataset
    df_enhanced = enhance_dataset(df)
    
    # Save enhanced dataset
    df_enhanced.to_csv('data_jobs_enhanced.csv', index=False)
    
    print(f"Enhanced dataset saved with {len(df_enhanced.columns)} columns")
    print(f"New columns added: {[col for col in df_enhanced.columns if col not in df.columns]}")