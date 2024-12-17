import converter
import transcribator


def seconds_to_minutes_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    result = f"{minutes}:{remaining_seconds:02d}"
    return result


def transcribize(file_path: str):
    wav_path = converter.convert_audio(file_path)
    return transcribator.transcribize_wav_text(wav_path)


def transcribize_timestamps(file_path: str, output_name: str):
    wav_path = converter.convert_audio(file_path)
    transcriprion = transcribator.transcribize_wav_chunks(wav_path)
    full_text = "(" + seconds_to_minutes_seconds(int(transcriprion[0]["timestamp"][0])) + ", "
    current_sentence = ""
    for i in range(len(transcriprion)):
        current_sentence += transcriprion[i]["text"]
        if transcriprion[i]["text"][-1] == "." or transcriprion[i]["text"][-1] == "?":
            full_text += seconds_to_minutes_seconds(
                int(transcriprion[i]["timestamp"][1])) + ")" + current_sentence + "\n"
            current_sentence = ""
            if i != len(transcriprion) - 1:
                full_text += "(" + seconds_to_minutes_seconds(int(transcriprion[i]["timestamp"][0])) + ", "
    with open(output_name + ".txt", "w", encoding="utf-8") as file:
        file.write(full_text)
    with open("/start_texts/start_transcription.txt", "w", encoding="utf-8") as file:
        file.write(full_text)
