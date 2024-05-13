import random
import string
import pandas
import json
# from generate_resource_data import certificates, majors

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
    },
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


class Task:
    def __init__(self, task_id, task_type, description, pre_tasks, requirements, affected_factors):
        self.task_id = task_id
        self.task_type = task_type
        self.description = description
        self.pre_tasks = pre_tasks
        # self.duration = duration
        # self.weights = weights
        self.requirements = requirements
        self.affected_factors = affected_factors

    def __repr__(self):
        return f"Task(TaskID: {self.task_id}, TaskType: {self.task_type}, PreTasks: {self.pre_tasks}, Weights: {self.weights}, Requirements: {self.requirements}, AffectedFactors: {self.affected_factors})"


# Function to generate random task data
def generate_random_task(task_id):
    task_type = random.choice(["Type A", "Type B", "Type C"])
    description = "Description task " + str(task_id)
    pre_tasks = random.sample(
        [num for num in range(1, 251) if num != task_id], 200)
    # # Duration in hours with steps of 0.25
    # duration = round(random.uniform(1, 72), 2)
    # duration = round(duration * 4) / 4  # Round to the nearest 0.25
    # weights = {str(random.randint(1, 2837)): round(random.uniform(0, 1), 2)
    #            for i in range(1, random.randint(2, 6))}

    # Generate random certificates for the task
    certificates_count = 1
    certificates_selected = random.sample(certificates, certificates_count)

    # Generate random majors for the task
    majors_selected = random.sample(majors, 1)

    majors_type_selected = random.sample(type_majors, 1)

    requirements = {
        "certificates": [],
        "majors": '',
        "type_majors": ''
    }

    # product_id = random.randint(1, 10)
    # environment_id = random.randint(11, 20)
    # while environment_id == product_id:
    #     environment_id = random.randint(11, 20)

    # affected_factors = [(product_id, "Product", random.randint(
    #     1, 5)), (environment_id, "Environment", random.randint(1, 5))]

    product_id = list(range(1, 11))  # Create a list from 1 to 10


    environment_id = list(range(11, 21))  # Create a list from 11 to 20

    # random.shuffle(product_id)  # Shuffle the product_id list
    # random.shuffle(environment_id)  # Shuffle the environment_id list

    # # Generate random numbers for environment_id until it is different from any value in product_id
    # while any(env_id in product_id for env_id in environment_id):
    #     random.shuffle(environment_id)

    # Create affected_factors list with tuples of (ID, Type, Random Number)
    affected_factors = [(product_id[i], "Product", random.randint(1, 5)) for i in range(len(
        product_id))] + [(environment_id[i], "Environment", random.randint(1, 5)) for i in range(len(environment_id))]

    # print(affected_factors)

    return {
        "TaskID": task_id,
        "TaskType": task_type,
        "Description": description,
        "PreTasks": pre_tasks,
        "Requirements": json.dumps(requirements),
        "AffectedFactors": json.dumps(affected_factors)
    }


# Function to create Task instances from data
def create_tasks(data):
    tasks = []
    for task_info in data:
        task = Task(
            task_info["TaskID"],
            task_info["TaskType"],
            task_info["Description"],
            task_info["PreTasks"],
            task_info["Requirements"],
            task_info["AffectedFactors"]
        )
        tasks.append(task)
    return tasks


# Generating random task data
random_tasks_data = [generate_random_task(i) for i in range(1, 251)]

# Creating tasks from random data
random_tasks = create_tasks(random_tasks_data)

# Convert the list of tasks to a list of dictionaries
tasks_data = [task.__dict__ for task in random_tasks]

# # Convert the list of dictionaries to a DataFrame
# df = pd.DataFrame(tasks_data)


# print(tasks_data)
# Convert the list of dictionaries to a DataFrame
df = pandas.DataFrame(tasks_data)

# Write DataFrame to CSV
df.to_csv("exported_data/tasks.csv", index=False)

print("CSV file 'random_tasks.csv' has been created.")
