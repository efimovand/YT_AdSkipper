import whisper
from pytube import YouTube
from datetime import datetime
import os


AUDIO_SAVE_DIRECTORY = "/Users/andrey/PycharmProjects/testWhisper/downloads"

def download_audio(video_url):

    # Скачивание звука из ВИДЕО
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio = True).first()
    try:
        audioFile = audio.download(AUDIO_SAVE_DIRECTORY)
        print("Audio was downloaded successfully")
    except:
        print("Failed to download audio")
        return

    # Преобразование ЗВУКА в ТЕКСТ
    try:
        saved_time = datetime.now()

        model = whisper.load_model("base")
        result = model.transcribe(audioFile, fp16=False)
        segments = result["segments"]
        print(result, "\n")

        print(f'Finished Transcribing [{round((datetime.now() - saved_time).total_seconds(), 1)}sec | {segments[-1]["end"]}sec]')  # Время выполнения
    except:
        print("Failed to transcribe audio")
        return

    # Поиск рекламных вставок
    # for i in segments:
    #     print(i["text"])

    # Очистка папки с загрузками
    directory = '/Users/andrey/PycharmProjects/testWhisper/downloads'
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))


download_audio("https://www.youtube.com/watch?v=GlAaNG6H17Y")
