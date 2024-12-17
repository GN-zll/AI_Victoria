import os
from pydub import AudioSegment


def convert_audio(file_path: str) -> str:
    """ Конвертирует аудиофайл в расширение .wav для передачи в модель.

        Args:
            file_path: путь до аудиофайла

        Returns:
            Возвращает новый путь до файла с расширением .wav
    """
    wav_path = file_path
    if file_path.endswith((".mp3", ".m4a", ".ogg", ".flac", ".aac", ".wav")):
        # Независимо от формата файла, создаем путь с .wav
        wav_path = file_path.rsplit(".", 1)[0] + ".wav"
        # Преобразование файла в формат wav, одноканальный и 16 кГц
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_channels(1).set_frame_rate(16000)

        # Экспортируем в wav
        audio.export(wav_path, format="wav")

    return wav_path  # Сохранение пути к новому файлу