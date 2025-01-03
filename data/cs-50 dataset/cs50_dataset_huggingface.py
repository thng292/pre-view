import json
import os
from pydub import AudioSegment
from datasets import Dataset, Audio, concatenate_datasets
import json

path = "data/"
file_names = [f for f in os.listdir(path) if f.endswith('-fix.json')]
for idx,fileName in enumerate(file_names):
    processed_clips = []
    texts = []
    durs = []
    fileName = path + fileName.replace("-fix.json", "")
    json_file_path = f"{fileName}-fix.json"
    input_audio_path = f"{fileName}.m4a"
    output_directory = f"{fileName}/"  

    with open(json_file_path, "r") as file:
        subtitles = json.load(file)
    audio = AudioSegment.from_file(input_audio_path, format="m4a")

    os.makedirs(output_directory, exist_ok=True)

    for i, entry in enumerate(subtitles):
        start_time_ms = int(entry["start"] * 1000)
        end_time_ms = start_time_ms + int(entry["duration"] * 1000) + 50

        segment = audio[start_time_ms:end_time_ms]

        output_path = f"{output_directory}clip_{i + 1}.wav"
        segment.export(output_path, format="wav")
        print(f"Exported: {output_path}")

        processed_clips.append(output_path)
        texts.append(entry['text'])
        durs.append(entry['duration'])
    audio_dataset = Dataset.from_dict({"audio": processed_clips, "text": texts, "duration": durs}).cast_column("audio", Audio())
    dataset_output_path = f"{fileName}-dataset"
    audio_dataset.save_to_disk(dataset_output_path)