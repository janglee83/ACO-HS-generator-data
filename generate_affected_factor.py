import pandas as pd

product_count = 0
environment_count = 0
count = 0

data_set = []

# Define function to generate ID


def generate_id(type):
    global count, product_count, environment_count
    count += 1
    if type == "Product":
        product_count += 1
        return product_count
    elif type == "Environment":
        environment_count += 1
        return environment_count
    else:
        return None


# Add products
for i in range(10):
    product_id = generate_id("Product")
    product_description = f"Product {product_id} description"
    data_set.append({"ID": count, "Type": "Product",
                    "Description": product_description})

# Add environments
for i in range(10):
    environment_id = generate_id("Environment")
    environment_description = f"Environment {environment_id} description"
    data_set.append({"ID": count, "Type": "Environment",
                    "Description": environment_description})

# Convert to DataFrame
df = pd.DataFrame(data_set)

# Save to CSV
df.to_csv("exported_data/affected_factors_dataset.csv", index=False,
          columns=["ID", "Type", "Description"])
