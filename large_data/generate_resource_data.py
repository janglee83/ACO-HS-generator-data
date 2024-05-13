# build generate resource function
import random
import pandas
import json

# List of common first names and last names
first_names = ["John", "Jane", "Michael", "Emily", "William", "Emma", "Alexander", "Olivia", "James",
               "Sophia", "Daniel", "Isabella", "David", "Mia", "Joseph", "Charlotte", "Samuel", "Ella", "Benjamin", "Grace",
               "Jacob", "Ava", "Matthew", "Abigail", "Andrew", "Madison", "Ethan", "Sofia", "Christopher", "Chloe",
               "Joshua", "Evelyn", "Ryan", "Harper", "Elijah", "Amelia", "Nathan", "Elizabeth", "Jonathan", "Lily",
               "Christian", "Avery", "Liam", "Eleanor", "Nicholas", "Addison", "Tyler", "Natalie"]

last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
              "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
              "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez",
              "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson",
              "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker"]


# List of certificates with scores
certificates = [
    {
        "name": "Offensive Security Certified Expert",
        "abbreviation": "OSCE",
    },
    {
        "name": "Offensive Security Certified Professional",
        "abbreviation": "OSCP",
    },
    {
        "name": "Certified Ethical Hacker",
        "abbreviation": "CEH",
    },
    {
        "name": "Certified Information System Security Professional",
        "abbreviation": "CISSP",
    },
    {
        "name": "Computer Hacking Forensic Investigator",
        "abbreviation": "CHFI",
    },
    {
        "name": "CREST Practitioner Security Analyst",
        "abbreviation": "CSPA",
    },
    {
        "name": "EC-Council Certified Security Analyst",
        "abbreviation": "CSPA",
    }
]

# List of majors with their English versions
majors = [
    {
        "name": "Công nghệ thông tin",
        "english_name": "Information Technology",
        "abbreviation": "IT",
    },
    {
        "name": "Máy tính",
        "english_name": "Computer Science",
        "abbreviation": "CS",
    },
    {
        "name": "Toán học",
        "english_name": "Mathematics",
        "abbreviation": "Math",
    },
    {
        "name": "Kỹ thuật điện, điện tử và viễn thông",
        "english_name": "Electrical, Electronics, and Telecommunications Engineering",
        "abbreviation": "EE&TC Eng",
    },
    {
        "name": "Khoa học dữ liệu",
        "english_name": "Data Science",
        "abbreviation": "DS",
    }
]

type_majors = [
    {
        "name": "Trung bình",
        "english_name": "Average",
        "abbreviation": "Avg",
    },
    {
        "name": "Khá",
        "english_name": "Good",
        "abbreviation": "Good",
    },
    {
        "name": "Giỏi",
        "english_name": "Excellent",
        "abbreviation": "Excel",
    },
    {
        "name": "Xuất sắc",
        "english_name": "Outstanding",
        "abbreviation": "Outst",
    },
]

# Function to generate a random name
def generate_random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

# Function to generate random certificates for qualifications


def generate_certificates():
    num_certificates = 7
    return random.sample(certificates, num_certificates)

# Function to generate random major for qualification


def generate_major():
    return random.choice(majors)

def generate_type_major():
    return random.choice(type_majors)


# Define attributes and their possible values
attributes = {
    "certificates": certificates,  # Add certificates as an attribute
    "major": majors,  # Add major as an attribute
    "type_major": type_majors
}

# Generate random qualifications for each resource


def generate_qualification():
    qualifications = []
    for attribute, values in attributes.items():
        if attribute == "certificates":
            certs = generate_certificates()
            for cert in certs:
                qualifications.append(
                    {'Certificate': cert['abbreviation']})
        elif attribute == "major":
            major = generate_major()
            qualifications.append(
                {'Major': major['abbreviation']})
        elif attribute == "type_major":
            type_major = generate_type_major()
            qualifications.append({"Type_Major": type_major['abbreviation']})
    return qualifications

# Generate random experience for each resource


def generate_experience():
    experience = []
    task_types = range(1, 251)  # Task IDs from 1 to 1000
    for task_type in task_types:
        lower_bound = random.uniform(0, 0.5)
        upper_bound = random.uniform(lower_bound, 1)
        payload = {
            'task_id': task_type,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,

        }
        experience.append(payload)
    return experience

# Generate dataset with specified number of resources


def generate_dataset(num_resources):
    dataset = []

    for i in range(num_resources):
        resource = {}
        qualifications = generate_qualification()
        resource["Resource_Id"] = i + 1
        resource["Type"] = "Human"
        resource["Description"] = generate_random_name()
        resource['Qualifications'] = json.dumps(qualifications)
        experience = generate_experience()
        resource['Experience'] = json.dumps(experience)
        dataset.append(resource)
        # for qualification in qualifications:
        #     resource = {}
        #     resource["Type"] = "Human"
        #     resource["Description"] = generate_random_name()
        #     resource["Qualification_Name"] = qualification['Qualification_Name']
        #     resource["Qualification_Value"] = qualification['Qualification_Value']
        #     experience = generate_experience()
        #     for exp in experience:
        #         experience_dict = {}
        #         experience_dict["Task_id"] = exp["task_id"]
        #         experience_dict["Lower_bound"] = exp["lower_bound"]
        #         experience_dict["Upper_bound"] = exp["upper_bound"]

        #         dataset.append({ **resource, **experience_dict })

        # print(i)

    return dataset


# Generate a dataset with 10 resources
dataset = generate_dataset(50)

# Convert dataset to Pandas DataFrame
df = pandas.DataFrame(dataset)

# Write DataFrame to CSV file
csv_file = "exported_data/resources.csv"
df.to_csv(csv_file, index=False)

print(f"Dataset written to {csv_file}")

