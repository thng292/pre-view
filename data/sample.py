import datasets, csv
from dotenv import load_dotenv
load_dotenv()

# Open the CSV file
with open('leetcode_problems_raw.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)

    # Convert the reader to a list of dictionaries
    data = [row for row in csv_reader]

data = datasets.Dataset.from_list(data)
col_name = data.column_names
for name in col_name:
    data = data.rename_column(name, name.lower().replace(' ', '_'))
print(data)
data = data.filter(lambda e: e['paid_only'] != 'True')
data.remove_columns(['paid_only'])
print(data)
data.push_to_hub("pre-view/leetcode_demo", max_shard_size="2GB")
