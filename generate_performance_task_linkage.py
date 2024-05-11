import pandas
import json
import random

kpi_pd = pandas.read_csv('exported_data/KPI_data.csv')
task_pd = pandas.read_csv('exported_data/tasks.csv')
resource_pd = pandas.read_csv('exported_data/resources.csv')

num_metrics_kpi = 570
num_global_kpi = 100

# print(resource_pd['Qualifications'])


def get_resource_base_condition(certi, major, type_majors):
    def get_list_resource_id_base_list(list_item):
        item_list = list()
        for item in list_item:
            item_list.append(item['Resource_Id'])
        return item_list

    list_fit_major = list()
    for index_resource, resource_data in resource_pd.iterrows():
        for item in json.loads(resource_data['Qualifications']):
            for key, value in item.items():
                if key == 'Major' and major == value:
                    list_fit_major.append(resource_data)

    list_fit_major_and_type_major = list()
    for resource_data in list_fit_major:
        for item in json.loads(resource_data['Qualifications']):
            for key, value in item.items():
                if key == 'Type_Major' and value == type_majors:
                    list_fit_major_and_type_major.append(resource_data)

    if len(certi) == 0:
        return get_list_resource_id_base_list(list_fit_major_and_type_major)

    list_final = list()
    for resource_data in list_fit_major_and_type_major:
        certi_list = list()
        for item in json.loads(resource_data['Qualifications']):
            for key, value in item.items():
                if key == 'Certificate':
                    certi_list.append(value)

        if set(certi).issubset(set(certi_list)) is True:
            list_final.append(resource_data)

    return get_list_resource_id_base_list(list_final)


def generate_normalized_array(original_array_len):
    # Generate random numbers
    random_array = [random.random() for _ in range(original_array_len)]

    # Normalize the random numbers to ensure their sum equals 1
    total = sum(random_array)
    normalized_array = [x / total for x in random_array]

    return normalized_array


def fit_resource_for_task(task_id: int):
    task_result = task_pd[task_pd['task_id'] == task_id]
    temp = json.loads(task_result['requirements'].iloc[0])
    certi = temp['certificates']
    major = temp['majors']
    type_majors = temp['type_majors']
    resource_ids = get_resource_base_condition(
        certi=certi, major=major, type_majors=type_majors)

    return resource_ids

list_csv = list()

for kpi_global_id in range(1, num_global_kpi + 1):
    filter_value = kpi_pd[kpi_pd['KPI_Goal_Id'] == kpi_global_id]
    start_num = (kpi_global_id - 1) * 5 + 1
    end_num = start_num + 4

    get_list_task = list(range(start_num, end_num + 1))

    final_list = list()

    weight_task = generate_normalized_array(len(get_list_task))

    for index, row in filter_value.iterrows():
        payload = {}
        payload['KPI_Metric_Id'] = row['KPI_Metric_Id']
        payload['list_task'] = list()

        for index, item_task_id in enumerate(get_list_task):
            task_payload = {}
            task_payload['task_id'] = item_task_id
            resource_ids = fit_resource_for_task(item_task_id)
            task_payload['resource_ids'] = resource_ids
            task_payload['durations_resource_ids'] = [random.randint(
                1, 300) * 0.25 for _ in range(len(resource_ids))]
            task_payload['task_weight'] = weight_task[index]

            payload['list_task'].append(task_payload)

        final_list.append(payload)
    list_csv.append(final_list)

# Convert dataset to Pandas DataFrame
# df = pandas.DataFrame(list_csv)
# print(df)

# # Write DataFrame to CSV file
# csv_file = "exported_data/resources.csv"
# df.to_csv(csv_file, index=False)

# print(f"Dataset written to {csv_file}")

# Initialize an empty dataframe
df = pandas.DataFrame(columns=['KPI_Metric_Id', 'Task_ID',
                  'Resource_IDs', 'Durations_Resource_IDs', 'Task_Weight'])

# Iterate through each element in list_csv
for sublist in list_csv:
    for item in sublist:
        # Extract KPI_Metric_Id from the payload
        kpi_metric_id = item['KPI_Metric_Id']

        # Extract list_task from the payload
        list_task = item['list_task']

        # Iterate through each task in list_task
        for task in list_task:
            # Extract task_id, resource_ids, durations_resource_ids, and task_weight from task
            task_id = task['task_id']
            resource_ids = task['resource_ids']
            durations_resource_ids = task['durations_resource_ids']
            task_weight = task['task_weight']

            # Append a new row to the dataframe
            df = df._append({'KPI_Metric_Id': kpi_metric_id,
                            'Task_ID': task_id,
                            'Resource_IDs': resource_ids,
                            'Durations_Resource_IDs': durations_resource_ids,
                            'Task_Weight': task_weight}, ignore_index=True)

# Define the filename for your CSV file
csv_filename = 'exported_data/performance_task_linkage.csv'

# Write the dataframe to a CSV file
df.to_csv(csv_filename, index=False)

print("CSV file generated successfully!")
