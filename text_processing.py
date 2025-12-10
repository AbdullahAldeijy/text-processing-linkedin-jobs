# Import packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import warnings
import re
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_excel('Linkedin Job Posts in Saudi Arabia 2020.xlsx')

# Define special characters to remove from dataset
spec_chars = ["!", '"', "#", "%", "&", "'", "(", ")",
              "*", "+", ",", "-", ".", "/", ":", ";", "<",
              "=", ">", "?", "@", "[", "\\", "]", "^", "_",
              "`", "{", "|", "}", "~", "–"]

# Extract date components
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter

# Clean location data by removing special characters
for char in spec_chars:
    df['location'] = df['location'].str.replace(char, ' ')

# Extract first word from location column as city
df['city'] = df['location'].str.split(' ').str[0]

print(f"Unique cities: {df['city'].nunique()}")

# Convert blank space to null values
df['city'] = df['city'].replace(r'', np.nan)

# Fill null values
df['city'] = df['city'].fillna('NotDefined')

for char in spec_chars:
    df['city'] = df['city'].str.replace(char, '')

print(f"Cities after cleaning: {df['city'].nunique()}")

# Add new column region - extract first word from city column
df['Regions'] = df['city'].str.split(' ').str[0]

df.loc[df['Regions'].str.contains('Jeddah|Makkah|Rabigh|Taif|Thuwal|Dhahban|AlKhurmah|AlLith'), 'Regions'] = 'Makkah'
df.loc[df['Regions'].str.contains('Riyadh|AlKharj|AlHair|AlMajma|AlDuwadimi|AlQuwayiyah|Shaqra|AlAflaj|Afif|AlDiriyah|Huraymila|Zulfi|UmmalHamam'), 'Regions'] = 'Riyadh'
df.loc[df['Regions'].str.contains('Dammam|AlKhobar|Alsharqiyah|Jubail|Dhahran|Khobar|RasTanura|Abqaiq|Qatif|AlHufuf|Ahsa|Safwa|Khafji|Harad|Umm_al-Hamam|Saihat|AlMubarraz|HafarAlbatin'), 'Regions'] = 'Eastern'
df.loc[df['Regions'].str.contains('Khamis_Mushait|Abha|AlMajardah|MahayelAseer|AlFarah|Balqarn|Bisha|SaratUbaida|AlNamas|KhamisMushait'), 'Regions'] = 'Asir'
df.loc[df['Regions'].str.contains('Jazan|AlShuqaiq|Baysh'), 'Regions'] = 'Jazan'
df.loc[df['Regions'].str.contains('Madinah|Yanbu|Badr|Hinakiyah|Al-Ula|AlUla'), 'Regions'] = 'Medina'
df.loc[df['Regions'].str.contains('Buraydah|AlQassim|AlMuthneb|Albadai|Albukairyah|Unayzah'), 'Regions'] = 'AlQassim'
df.loc[df['Regions'].str.contains('Tabuk|AlWajh|Neom|Duba'), 'Regions'] = 'Tabuk'
df.loc[df['Regions'].str.contains('Hail'), 'Regions'] = 'Hail'
df.loc[df['Regions'].str.contains('Najran|Sharorah|Yadma'), 'Regions'] = 'Najran'
df.loc[df['Regions'].str.contains('Sakakah|Qurayyat|DumatAlJandal'), 'Regions'] = 'AlJawf'
df.loc[df['Regions'].str.contains('AlBahah|AlAin'), 'Regions'] = 'AlBahah'
df.loc[df['Regions'].str.contains('Turaif|Rafha|Arar'), 'Regions'] = 'Northern Borders'
df.loc[df['Regions'].str.contains('NotDefined'), 'Regions'] = 'NotDefind'
df.loc[df['Regions'].str.contains('Remote|LeMéridien'), 'Regions'] = 'Remote'

pd.options.display.max_rows = 4000
print(f"Regions distribution: {df['Regions'].nunique()} unique regions")

for char in spec_chars:
    df['industries'] = df['industries'].str.replace(char, '')

# Replace blank space column to null values
df['industries'] = df['industries'].replace(r'', np.nan)

# Drop null values
df = df.dropna(subset=['industries'])

print(f"Industries unique count: {df.industries.nunique()}")

# Extract industry categories
df['industry_cat'] = df['industries'].str.extract(
    r'(Administrative|Business Supplies and Equipment|Chemicals|Business Development|Building Materials|Capital Markets|Banking|Aviation|Biotechnology|Broadcast Media|Automotive|Arts and Crafts|Architecture|Apparel|Animation|Accounting|Market Research|Oil|Insurance|Hospitality|Food Production|Food|Information Technology and Services|Hospital|Fashion|Financial Services|Airlines|Civic|Civil Engineering|Commercial Real Estate|Computer|Construction|Consulting|Consumer Electronics|Consumer Goods|Consumer Services|Cosmetics|Customer Service Sales|Dairy|Defense|Design|ELearning|Education|Electrical|Entertainment|Environmental Services|Events Services|Executive Services|Facilities Services|Farming|Fine Art|Furniture|Graphic Design|Glass Ceramics|Government Administration|Government Relations|Human Resources|Health Care Provider|Individual|Information Services|Internet|Investment|Law|Legal Service|Leisure Travel|Logistic and Supply Chain|Luxury Goods|Machinery|Marketing and Advertising|Management Consulting|Media|Medical|Mental Health Care|Military|Mobile Game|Music|Museums|Nanotechnology|Newspapers|Online Media|Real Estate|Security|Retail|Sports|Supermarkets|Telecommunication|Writing|Warehousing|Utilites|Venture Capital|Wholesale|Sporting Goods|Research|Publishing|Public Safety|Public Policy|Public Relations|Photography|Packaging and Containers|Quality Assurance|Purchasing Supply Chain|Outsourcing|Pharmaceuticals|Plastics|Training|Motion Pictures|International Trade|International Affairs|Import and Export|Industrial Automation|Maritime|Mechanical|Program Development|Project Management|Mining|Philanthropy|Printing|Transportation|Restaurants|Health Wellness and Fitness|Paper|Higher Education|Renewables|Semiconductors|Staffing and Recruiting|Textiles|Tobacco|Translation and Localization|Veterinary|Alternative Dispute Resolution|Analyst)')

print(df['industry_cat'].value_counts())

# Drop null values
df = df.dropna(subset=['industry_cat'])

print(df['industry_cat'].unique())

# Replace blank space column to null values
df['industry_cat'] = df['industry_cat'].replace(r'', np.nan)

# Define function to remove unwanted characters
def remove_unwanted_characters(s):
    s = re.sub('\\*', ' ', str(s))
    s = re.sub('/', ' ', str(s))
    s = re.sub('_', ' ', str(s))
    s = re.sub('\\?', ' ', str(s))
    s = re.sub('%', ' ', str(s))
    s = re.sub('@', ' ', str(s))
    s = re.sub('#', ' ', str(s))
    s = re.sub('!', ' ', str(s))
    s = re.sub(',', ' ',str(s))
    s = re.sub('\\+', ' ', str(s))
    s = re.sub('&', ' ', str(s))
    return s

# Remove common text in job description
def rem_fluff(data):
    data = data.replace('please share resume', " ")
    data = data.replace('call me', " ")
    data = data.replace('if you are a', " ")
    data = data.replace('if you are an', " ")
    data = data.replace('job description', " ")
    data = data.replace('if you are', " ")
    data = data.replace('reply', " ")
    data = data.replace("please apply today applicants must be authorized to work in the u.s.please apply directly to by clicking 'click here to apply' with your word resume looking forward to receiving your resume and going over the position in more detail with you.- not a fit for this position click the link at the bottom of this email to search all of our open positions.looking forward to receiving your resume cybercoderscybercoders inc is proud to be an equal opportunity employerall qualified applicants will receive consideration for employment without regard to race color religion sex national origin disability protected veteran status or any other characteristic protected by law.your right to work - in compliance with federal law all persons hired will be required to verify identity and eligibility to work in the united states and to complete the required employment eligibility verification document form upon hire.copyright  - . cybercoders inc. all rights reserved.", ' ')
    return data

# function to get rid of repeated skills after a '-'
def split_skills(data):
        x = data
        nospace = x.replace(' ', '') # removing spaces
        if '-' in nospace:
            first_half = nospace.split('-')[0] #first half of string before '-'
            second_half = nospace.split('-')[1] # second half of string after '-'
            if first_half == second_half:
                x = list(x.split('-'))[0].strip() #getting only first half of string to return
                return x
            else:
                return x
        else:
            return x

def drop_corrupt_rows(df):
    df['word_count'] = df['description'].map(lambda x: len(x.split()))

    mean_word_count = df['word_count'].mean()
    print('Mean word count per post:', round(mean_word_count))

    std_word_count = df['word_count'].std()
    print('std word count per post:', round(std_word_count))

    too_short = mean_word_count - 1.5*std_word_count
    too_short = 20

    # Drop posts with 20 word or less
    print(len(df), 'before dropping')
    mask = df['word_count'] > too_short
    df = df[mask]
    print(len(df), 'after dropping')

    df.drop(columns='word_count', inplace=True)

    return df.reset_index(drop=True)

# Remove unwanted characters and numbers
df['description'] = df['description'].map(remove_unwanted_characters)
df['industries'] = df['industries'].map(remove_unwanted_characters)

# Correct multiple spaces (including \t and \n)
df['description'] = df['description'].map(lambda x: re.sub(r'[^a-zA-Z0-9]',' ', x))
df['industries'] = df['industries'].map(lambda x: re.sub(r'[^a-zA-Z0-9]',' ', x))

# Drop corrupted rows
df = drop_corrupt_rows(df)

# Remove common phrases
df['description'] = df['description'].map(rem_fluff)
df['industries'] = df['industries'].map(rem_fluff)

df['description'] = df['description'].str.lower()

#Number of unique entries were found for each columns.
df.apply(pd.Series.nunique)

df[['description']]= df[['description']].dropna()

def years_of_ex(description):
    if description != np.nan:
        description = description.lower()
        match = re.search('[^0-9]\\+ years|[^0-9]\\+ year|[0-9] [0-9]\\+ years|[0-9] [0-9]\\+ year|\\+[0-9]|[0-9] to [0-9] year|[0-9] to [0-9] years|[0-9] to [0-9] yrs|[0-9] [0-9] yrs|[^0-9] +year|[0-9] +years|..\\+ yrs|[0-9] [0-9] +years|entry|junior', description)
        if match != None:
            return description[match.start(): match.end()]
    return np.nan

df['years_of_ex'] = df['description'].apply(years_of_ex)
print(df['years_of_ex'].isnull().sum())

# Extract numbers
df['year_of_ex']=df['years_of_ex'].str.extract('(\\d)')

#change data type to calculate the mean
df['year_of_ex'] = df['year_of_ex'].astype(float)

#calculate the mean of experience according to level grouping
years=df.groupby('level').agg(years_of_ex = ('year_of_ex', 'mean'))

#fill null values with mean
df['year_of_ex']=df['year_of_ex'].fillna(df.groupby('level')['year_of_ex'].transform('mean'))

# Fill any remaining NaN values with 0
df['year_of_ex'] = df['year_of_ex'].fillna(0)

#convert years_experience from float to int
df['year_of_ex'] = df['year_of_ex'].astype(int)

#remove stopword from description
spec_char=["in","or","and","from","is","a","that","with","at","of"]
for chars in spec_char:
    df['description'] = df['description'].str.replace(chars, '')

def degree(description):
    if description != np.nan:
        description = description.lower()
        match = re.search(r'bachelor|master|masters| ms | bs | phd | msc |university|technicl degree|mster|bchel|bchels|msters|diplom| hve |needbchels|experiencebchels|requirementsbchels|college|qulifictionsbchels|electricl |undergrdute|grdute|mechnicl', description)
        if match != None:
            return description[match.start(): match.end()]
    return np.nan

df['degree'] = df['description'].apply(degree)
print(df['degree'].isnull().sum())

df['degree'] = df['degree'].str.replace(' ','')

df['degree'] = df['degree'].str.replace('undergrdute','student')

#bachelor
df['degree'] = df['degree'].str.replace('needbchels','bachelor')
df['degree'] = df['degree'].str.replace('experiencebchels','bachelor')
df['degree'] = df['degree'].str.replace('requirementsbchels','bachelor')
df['degree'] = df['degree'].str.replace('qulifictionsbchels','bachelor')

bachelor1=["bchel","bs","grdute","college","university"]
for chars12 in bachelor1:
    df['degree'] = df['degree'].str.replace(chars12,'bachelor')

#master
master1=["master","msc","masters","ms","mster","msters","masterter"," master"]
for chars1 in master1:
    df['degree'] = df['degree'].str.replace(chars1,'master')

#diploma
diploma1=["technicldegree","electricl","mechnicl"]
for chars11 in diploma1:
    df['degree'] = df['degree'].str.replace(chars11,'diplom')

#phd
df['degree'] = df['degree'].str.replace('phd','Doctorate')

#hve
df['degree'] = df['degree'].str.replace('hve','Higher Vocational Education')

#change diplom to diploma
df['degree'] = df['degree'].str.replace('diplom','diploma')

df['degree_int']=df['degree'].str.extract('(Higher Vocational Education|bachelor|diploma|master|student|Doctorate)')

# add new column extracting values from degree and replace it with numbers to calculate the mean and fill null values with it
df['degree_int'] = df['degree_int'].str.replace('Higher Vocational Education','1')
df['degree_int'] = df['degree_int'].str.replace('bachelor','2')
df['degree_int'] = df['degree_int'].str.replace('diploma','3')
df['degree_int'] = df['degree_int'].str.replace('master','4')
df['degree_int'] = df['degree_int'].str.replace('student','5')
df['degree_int'] = df['degree_int'].str.replace('Doctorate','6')

df['degree_int']=df['degree_int'].replace(r'', np.nan)

#change data type to float to correctly calculate the mean
df['degree_int'] = df['degree_int'].astype(float)

df['degree_int']=df['degree_int'].fillna(df.groupby('level')['degree_int'].transform('mean'))

# Fill any remaining NaN values with 2 (bachelor level)
df['degree_int'] = df['degree_int'].fillna(2)

#convert float to int
df['degree_int'] = df['degree_int'].astype(int)

#convert float to int
df['degree_int'] = df['degree_int'].astype(str)

#replace the numbers back to string
df['degree_int'] = df['degree_int'].replace('1','Higher Vocational Education')
df['degree_int'] = df['degree_int'].replace('2','bachelor')
df['degree_int'] = df['degree_int'].replace('3','diploma')
df['degree_int'] = df['degree_int'].replace('4','master')
df['degree_int'] = df['degree_int'].replace('5','student')
df['degree_int'] = df['degree_int'].replace('6','Doctorate')

# Extract salary information
def extract_salary(description):
    if description != np.nan:
        description = description.lower()
        match = re.search(r'\\d+[,\\d]*\\s*(?:sar|riyal|sr|salary|k|thousand)', description)
        if match:
            return match.group()
    return np.nan

df['salary_mentioned'] = df['description'].apply(extract_salary)

# Extract common skills
def extract_skills(description):
    if description != np.nan:
        skills = []
        skill_patterns = ['python', 'java', 'sql', 'excel', 'powerbi', 'tableau', 'aws', 'azure', 'docker', 'react', 'nodejs', 'machine learning', 'data analysis']
        for skill in skill_patterns:
            if skill in description.lower():
                skills.append(skill)
        return ', '.join(skills) if skills else np.nan
    return np.nan

df['skills'] = df['description'].apply(extract_skills)

# Add useful metrics
df['description_length'] = df['description'].str.len()
df['is_remote'] = df['Regions'].str.contains('Remote').astype(int)

print(f"\\nFinal dataset info:")
print(f"Shape: {df.shape}")
print(f"Null values:\\n{df.isnull().sum()}")

print("\\n=== DATA SUMMARY ===")
print(f"Total jobs: {len(df):,}")
print(f"Jobs with salary info: {df['salary_mentioned'].notna().sum()}")
print(f"Jobs with skills: {df['skills'].notna().sum()}")
print(f"Remote jobs: {df['is_remote'].sum():,}")

#drop unneeded columns
df= df.drop(['degree'], axis=1)
df= df.drop(['degree_int'], axis=1)
df= df.drop(['years_of_ex'], axis=1)

# Export to CSV
df.to_csv('data_jobs.csv', index=False)
print("\\nProcessed data saved to 'data_jobs.csv'")
print(f"Final dataset shape: {df.shape}")
print(f"Final columns: {list(df.columns)}")