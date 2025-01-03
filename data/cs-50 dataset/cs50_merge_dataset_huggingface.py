from datasets import load_from_disk, concatenate_datasets
import os

path = './data/'
res = []
for datasetName in [f.name for f in os.scandir(path) if f.is_dir() and f.name.endswith('-dataset')]:
    print(f'loading {datasetName}')
    res.append(load_from_disk(path + datasetName))

merged_dataset = concatenate_datasets(res)
merged_dataset.save_to_disk(path + "finalDataset")