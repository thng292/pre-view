import google.generativeai as genai

MODEL = genai.GenerativeModel()


def speech_to_text(speech: bytes):
    return MODEL.generate_content(
        [
            {"mime_type": "audio/wav", "data": speech},
            "Generate audio diarization, including transcriptions only",
        ]
    ).text


if __name__ == "__main__":
    f = open("output.wav", "rb").read()
    print(speech_to_text(f))
