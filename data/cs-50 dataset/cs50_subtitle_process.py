import json
import os
import json


def normalizeText(sentence: str):
    sentence = sentence.replace('***', ' ').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    sentence = sentence.replace('>>', '').replace('--', ' ').strip()
    return ' '.join(sentence.split())

subtitleFlag = [
    '[DRAMATIC CHORD]',
    '[DRAMATIC MUSIC PLAYING]',
    '[HONKING]',
    '[AUDIO PLAYBACK]',
    '[LAUGHTER]',
    '[STRUMMED CHORD]',
    '[TYPING]', 
    '[MUSIC PLAYING]',
    '[AUDIO LOGO]', 
    '[Music]',
    '[MUSIC]', 
    '[APPLAUSE]', 
    '[VIDEO PLAYBACK]', 
    '[END PLAYBACK]',
    '[BANG]',
    '[BUZZER]',
    '[POP]'
]

speakerFlag = [
    "JORDAN HAYASHI:",
    "DAVID J. MALAN:",
    "SPEAKER 1:",
    "SPEAKER 7:",
    "SPEAKER 15:",
    "SPEAKER:",
    "RUPINDER:",
    "SIMON:",
    "DAVID MALAN:",
    "SPEAKER 2:",
    "SPEAKER 3:",
    "SPEAKER 4:",
    "SPEAKER 5:",
    "BRIAN YU:",
    "CARTER ZENKE:",
    "JORDAN:",
    "NICK PARLANTE:",
    "BINKY:"
]

path = "data/"
file_names = [f for f in os.listdir(path) if f.endswith('.json') and not f.endswith('-fix.json')]
for idx,fileName in enumerate(file_names):
    fileName = path + fileName.replace(".json", "")
    json_file_path = f"{fileName}.json"

    with open(json_file_path, "r") as file:
        subtitles = json.load(file)
    sentence = ""
    start_time_ms = 0
    duration = 0
    res = []
    for i, entry in enumerate(subtitles):
        entry['text'] = normalizeText(entry['text'])
        if entry['text'].startswith('.') or entry['text'].startswith('-'):
            entry['text'] = entry['text'][1:]
        if entry['text'] in subtitleFlag:
            if sentence != "":
                sentence = normalizeText(sentence)
                res.append({
                    'text': sentence,
                    'start': start_time_ms / 1000,
                    'duration': duration / 1000
                })
            sentence = ""
            duration = 0
            continue

        if sentence == "":
            start_time_ms = int(entry["start"] * 1000)

        duration += int(entry["duration"] * 1000)
        sentence += entry["text"]

        if duration < 3000:
            if not sentence.endswith(' '):
                    sentence += " "
            continue

        if i < len(subtitles) - 1 and int(subtitles[i + 1]["start"] * 1000) - (start_time_ms + duration) < 1000:
            if not sentence.endswith(('.', '?', '!')) or (i < len(subtitles) - 1 and subtitles[i + 1]['text'].startswith('And') and duration < 10000):
                if not sentence.endswith(' '):
                    sentence += " "
                continue
            
        sentence = normalizeText(sentence)
        res.append({
            'text': sentence,
            'start': start_time_ms / 1000,
            'duration': duration / 1000
        })
        sentence = ""
        duration = 0

    res2 = []
    for i, entry in enumerate(res):
        if entry['text'].find('[?') != -1 or entry['text'].find('[INAUDIBLE]') != -1:
            continue
        entry['text'] = entry['text'].replace('AUDIENCE: ', '').strip()
        for speaker in speakerFlag:
            entry['text'] = entry['text'].replace(speaker,'.').strip()
        for flag in subtitleFlag:
            entry['text'] = entry['text'].replace(flag,'.').strip()
        if entry['text'].startswith('.') or entry['text'].startswith('-'):
            entry['text'] = entry['text'][1:]
        entry['text'] = normalizeText(entry['text'])
        res2.append(entry)
    with open(fileName + '-fix.json', 'w', encoding='utf-8') as json_file:
        json.dump(res2, json_file, indent=4, ensure_ascii=False)