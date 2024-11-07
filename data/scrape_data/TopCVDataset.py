from datasets import Dataset

content = []

j = 0
for i in range(1, 9):
    with open(f'jobData{i}.txt', 'r') as file:
        current_element = []
        for line in file:
            if line.strip() == '----------------------------------':
                content.append({'content': '\n'.join(current_element).strip()})
                current_element = []
            else:
                current_element.append(line.strip())

    with open(f'jobLink{i}.txt', 'r') as file:
        for line in file:
            content[j]['link'] = line
            j += 1

dataset = Dataset.from_list(content)
print(dataset)
dataset.push_to_hub("cutehusky/JobDescriptionDataset")