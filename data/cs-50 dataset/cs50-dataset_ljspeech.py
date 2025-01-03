import os
import csv
import json
from pydub import AudioSegment

# Configuration
config = {
    "input": "./data/",
    "output_audio_dir": "./data/dataset/wavs",
    "metadata_file": "./data/dataset/metadata.csv",
}

def create_clips_and_metadata(config):
    # Prepare output directories
    os.makedirs(config["output_audio_dir"], exist_ok=True)

    file_names = [f for f in os.listdir(config["input"]) if f.endswith('-fix.json')]
    metadata_entries = []
    for idx,fileName in enumerate(file_names):
        fileName = fileName.replace("-fix.json", "")
        filePath = config["input"] + fileName
        json_file_path = f"{filePath}-fix.json"
        input_audio_path = f"{filePath}.m4a"

        # Load audio file
        audio = AudioSegment.from_file(input_audio_path)

        # Load subtitles JSON
        with open(json_file_path, "r") as f:
            subtitles = json.load(f)

        # Metadata collection
        for i, entry in enumerate(subtitles):
            # Extract text, start time, and duration
            text = entry["text"]
            start_time = entry["start"] * 1000  # Convert seconds to milliseconds
            duration = entry["duration"] * 1000  # Convert seconds to milliseconds
            end_time = start_time + duration

            # Extract audio clip
            clip = audio[start_time:end_time]

            # Save audio clip
            clip_filename = f"clip_{fileName}_{i + 1:04d}.wav"
            clip.set_frame_rate(22050)
            clip_filepath = os.path.join(config["output_audio_dir"], clip_filename)
            clip.export(clip_filepath, format="wav")

            # Append to metadata
            metadata_entries.append([clip_filename.replace('.wav', ''), text ,text])

    # Write metadata.csv
    with open(config["metadata_file"], "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["filename", "text", "normalized-text"])  # Header
        writer.writerows(metadata_entries)

    print(f"Processing complete!")
    print(f"Audio clips saved in: {config['output_audio_dir']}")
    print(f"Metadata file saved as: {config['metadata_file']}")


if __name__ == "__main__":
    create_clips_and_metadata(config)
