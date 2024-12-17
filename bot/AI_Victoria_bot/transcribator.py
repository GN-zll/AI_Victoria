"""
Транскрибация файлов расширения .wav
"""

import accelerate
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Импорт модели и процессора
model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
    chunk_length_s=10,
)

def transcribize_wav_chunks(file_path: str):
    """Транскрибация файлов расширения .wav.
    Использует whisper-large-v3 модель для задачи speech recognition на русском языке.
    
        Args:
            file_path: путь до аудиойфала
            
        Returns:
            transcription: текст транскрибации c таймкодами
    """
    transcription = pipe(file_path, return_timestamps=True, generate_kwargs={"language": "ru", "task": "transcribe", "return_timestamps":True})["chunks"]
    return transcription

def transcribize_wav_text(file_path: str):
    """Транскрибация файлов расширения .wav.
    Использует whisper-large-v3 модель для задачи speech recognition на русском языке.
    
        Args:
            file_path: путь до аудиойфала
            
        Returns:
            transcription: текст транскрибации
    """
    transcription = pipe(file_path, return_timestamps=True, generate_kwargs={"language": "ru", "task": "transcribe"})["text"]
    return transcription

