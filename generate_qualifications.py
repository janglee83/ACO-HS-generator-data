import pandas as pd
import random

# List of certificates with scores
certificates = [
    {
        "name": "Offensive Security Certified Expert",
        "abbreviation": "OSCE",
        "score": random.randint(1, 5)
    },
    {
        "name": "Offensive Security Certified Professional",
        "abbreviation": "OSCP",
        "score": random.randint(1, 5)
    },
    {
        "name": "Certified Ethical Hacker",
        "abbreviation": "CEH",
        "score": random.randint(1, 5)
    },
    {
        "name": "Certified Information System Security Professional",
        "abbreviation": "CISSP",
        "score": random.randint(1, 5)
    },
    {
        "name": "Computer Hacking Forensic Investigator",
        "abbreviation": "CHFI",
        "score": random.randint(1, 5)
    },
    {
        "name": "CREST Practitioner Security Analyst",
        "abbreviation": "CSPA",
        "score": random.randint(1, 5)
    },
    {
        "name": "EC-Council Certified Security Analyst",
        "abbreviation": "CSPA",
        "score": random.randint(1, 5)
    },
]

type_majors = [
    {
        "name": "Trung bình",
        "english_name": "Average",
        "abbreviation": "Avg",
        "score": 2
    },
    {
        "name": "Khá",
        "english_name": "Good",
        "abbreviation": "Good",
        "score": 3
    },
    {
        "name": "Giỏi",
        "english_name": "Excellent",
        "abbreviation": "Excel",
        "score": 4
    },
    {
        "name": "Xuất sắc",
        "english_name": "Outstanding",
        "abbreviation": "Outst",
        "score": 5
    },
]

# List of majors with their English versions
majors = [
    {
        "name": "Công nghệ thông tin",
        "english_name": "Information Technology",
        "abbreviation": "IT",
        "score": random.randint(1, 5)
    },
    {
        "name": "Máy tính",
        "english_name": "Computer Science",
        "abbreviation": "CS",
        "score": random.randint(1, 5)
    },
    {
        "name": "Toán học",
        "english_name": "Mathematics",
        "abbreviation": "Math",
        "score": random.randint(1, 5)
    },
    {
        "name": "Kỹ thuật điện, điện tử và viễn thông",
        "english_name": "Electrical, Electronics, and Telecommunications Engineering",
        "abbreviation": "EE&TC Eng",
        "score": random.randint(1, 5)
    },
    {
        "name": "Khoa học dữ liệu",
        "english_name": "Data Science",
        "abbreviation": "DS",
        "score": random.randint(1, 5)
    },
]

# Convert lists to DataFrames
certificates_df = pd.DataFrame(certificates)
majors_df = pd.DataFrame(majors)
type_majors_df = pd.DataFrame(type_majors)

# Add id column without altering the data
certificates_df.insert(0, 'id', certificates_df.reset_index().index + 1)
majors_df.insert(0, 'id', majors_df.reset_index().index + 1)
type_majors_df.insert(0, 'id', type_majors_df.reset_index().index + 1)


# Write DataFrames to CSV files
certificates_df.to_csv('exported_data/certificates.csv', index=False)
majors_df.to_csv('exported_data/majors.csv', index=False)
type_majors_df.to_csv('exported_data/type_majors.csv', index=False)
