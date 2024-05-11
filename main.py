import pandas
import random
import numpy

data_frame = pandas.read_csv(
    'Mayor_s_Management_Report_-_Agency_Performance_Indicators_20240505.csv')

list_column_to_remove = ['Agency', 'Retired', 'Source', 'Created On', 'Desired Direction',
                         'Geo Value', 'Frequency', 'Lag Time', 'Reporting Period', 'Critical', 'Fiscal Year', 'Value Date', 'Geo', 'Geo Type', 'Service', 'Additive', 'Target MMR2', 'Accepted Value YTD']

# remove column in data frame
data_frame.drop(list_column_to_remove, axis=1, inplace=True)

# Rename columns
data_frame.rename(columns={'Goal': 'KPI_Goal',
                           'Indicator': 'KPI_Metric',
                           'Description': 'KPI_Metric_Description',
                           'ID': 'KPI_ID',
                           'Parent ID': 'KPI_Goal_Id'}, inplace=True)

data_frame.sort_values(by='KPI_Goal_Id', inplace=True)

# Function to adjust 'Target MMR' based on condition
def adjust_target_mmr(row):
    if row['Measurement Type'] == 'Percentage':
        return 100
    elif row['Measurement Type'] == 'Number':
        return row['Accepted Value'] / random.uniform(0.7, 1)
    else:
        return row['Target MMR']


# Apply the function to each row
data_frame['Target MMR'] = data_frame.apply(adjust_target_mmr, axis=1)

result = data_frame.groupby('KPI_ID').agg({
    'Accepted Value': 'mean',
    'Target MMR': 'mean',
    # 'Agency Full Name': 'first',
    'KPI_Goal_Id': 'first',
    'KPI_Goal': 'first',
    'KPI_Metric_Description': 'first',
    # 'Measurement Type': 'first',
    'KPI_Metric': 'first'
}).reset_index()

result = result.dropna()

# Tạo một bản sao của DataFrame kết quả
result_reindexed = result.copy()

# Tạo một từ điển để ánh xạ giá trị cũ của KPI_Goal_Id sang giá trị mới
index_mapping = {}
new_index = 1
for old_index in result_reindexed['KPI_Goal_Id'].unique():
    index_mapping[old_index] = new_index
    new_index += 1


# Áp dụng ánh xạ vào DataFrame
result_reindexed['KPI_Goal_Id'] = result_reindexed['KPI_Goal_Id'].map(
    index_mapping)


# Tạo một bản sao của DataFrame kết quả
result_reindexed_KPI_ID = result_reindexed.copy()

# Tạo một từ điển để ánh xạ giá trị cũ của KPI_ID sang giá trị mới
kpi_id_mapping = {}
new_index = 1
for old_id in result_reindexed_KPI_ID['KPI_ID'].unique():
    kpi_id_mapping[old_id] = new_index
    new_index += 1

# Áp dụng ánh xạ vào DataFrame
result_reindexed_KPI_ID['KPI_ID'] = result_reindexed_KPI_ID['KPI_ID'].map(
    kpi_id_mapping)

result_reindexed_KPI_ID.rename(
    columns={"Accepted Value": "Real_Value", "Target MMR": "Planned_Value", "KPI_ID": "KPI_Metric_Id", "KPI_Goal": "KPI_Goal_Description"}, inplace=True)

# Add weight
result_reindexed_KPI_ID['Weight'] = 0.0

# Tính trọng số cho từng 'KPI_Goal_Id'
unique_goal_ids = result_reindexed_KPI_ID['KPI_Goal_Id'].unique()
for goal_id in unique_goal_ids:
    # Lấy ra các hàng tương ứng với 'KPI_Goal_Id' hiện tại
    subset = result_reindexed_KPI_ID[result_reindexed_KPI_ID['KPI_Goal_Id'] == goal_id]
    num_metrics = len(subset)

    # Gán trọng số
    if num_metrics == 1:
        result_reindexed_KPI_ID.loc[subset.index, 'Weight'] = 1
    else:
        weights = numpy.random.rand(num_metrics)
        weights /= weights.sum()  # Đảm bảo tổng trọng số là 1
        result_reindexed_KPI_ID.loc[subset.index, 'Weight'] = weights


result_reindexed_KPI_ID.to_csv('exported_data/KPI_data.csv', index=False,
                               columns=["KPI_Goal_Id", "KPI_Goal_Description", "KPI_Metric_Id", "KPI_Metric", "KPI_Metric_Description", "Planned_Value", "Real_Value", "Weight"])
