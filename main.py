import time

import ffmpeg
import whisper
from pytube import YouTube
from datetime import datetime
import os
from moviepy import editor
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from math import ceil

import telebot
client = telebot.TeleBot("5983419210:AAH4sym2SSb9-pg2M0xd7cZZNKOKNiB2qBs")  # Подключение ТГ БОТА
user = "899696208"  # ТГ ID


AUDIO_SAVE_DIRECTORY = "/Users/andrey/PycharmProjects/testWhisper/downloads"


# Преобразование ЗВУКА в ТЕКСТ
def transcribe(audioFile):
    try:
        saved_time = datetime.now()  # Текущее время для оценки времени работы
        model = whisper.load_model('base')
        result = model.transcribe(audioFile, fp16=False)

        # segments = result['segments']
        # print(result['text'], "\n")
        # if findAds(result['text']):
        #     return result['segments']
        # else:
        #     return False

        print(f'Finished Transcribing [{round((datetime.now() - saved_time).total_seconds(), 1)}sec | {result["segments"][-1]["end"]}sec]')  # Время выполнения

        return result['segments']

    except:
        print("Failed to transcribe audio")
        return


# Добавление в список только уникальных элементов (дубликаты полностью недопустимы)
def listWithoutDuplicates(element, list_set):
    if element not in list_set:
        list_set.append(element)
    else:
        list_set = [x for x in list_set if x != element]
    return list_set


# Анализ текста на наличие рекламы
def searchTextAds(segments_list):

    result_timings = []

    # triggers_A = ['описан', 'ссылка', 'промокод']
    # triggers_B = ['скидк', 'бонус']
    # triggers_C = ['хочу', 'рекоменд']

    triggers_A = ['жалуется']
    triggers_B = ['же']
    triggers_C = ['хочу', 'рекоменд']

    keepChain_B = False
    keepChain_C = False

    for segment in reversed(segments_list):

        text = segment['text'].lower()

        if any(word in text for word in triggers_A):
            result_timings = listWithoutDuplicates(segment['start'], result_timings)
            result_timings = listWithoutDuplicates(segment['end'], result_timings)
            keepChain_B = True
            keepChain_C = False

        elif any(word in text for word in triggers_B) and keepChain_B:
            result_timings = listWithoutDuplicates(segment['start'], result_timings)
            result_timings = listWithoutDuplicates(segment['end'], result_timings)
            keepChain_C = True

        elif any(word in text for word in triggers_C) and keepChain_C:
            result_timings = listWithoutDuplicates(segment['start'], result_timings)
            result_timings = listWithoutDuplicates(segment['end'], result_timings)

        else:
            keepChain_B = False
            keepChain_C = False

    result_timings.reverse()
    return result_timings


# Основной код
def checkVideo(video_url):

    # Скачивание звука из ВИДЕО
    saved_time = datetime.now()  # Текущее время для оценки времени работы
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio=True).first()
    try:
        audioFile = audio.download(AUDIO_SAVE_DIRECTORY)
        print(f"\nAudio was downloaded successfully [{round((datetime.now() - saved_time).total_seconds(), 1)}sec]\n")
    except:
        print("\nFailed to download audio\n")
        return

    # Разделение дорожки на короткие фрагменты
    clip = editor.AudioFileClip(audioFile)
    duration = temp_duration = clip.duration
    parts_amount = ceil(duration / 30)  # Количество фрагментов

    # Поочередный анализ каждого фрагмента на наличие рекламы
    for i in range (1, parts_amount + 1):

        print("PART", i)
        if temp_duration > 30:
            endTime = i * 30 + 30
        else:
            endTime = duration
        ffmpeg_extract_subclip(audioFile, i * 30, endTime, targetname='part.mp4')
        temp_duration -= 30

        segments = transcribe("part.mp4")  # Преобразование фрагмента в ТЕКСТ
        ads_timings = searchTextAds(segments)  # Поиск рекламы в тексте

        if ads_timings:  # Отправка таймингов пользователю, если ЕСТЬ реклама
            pass

    # Очистка папки с загрузками
    directory = '/Users/andrey/PycharmProjects/testWhisper/downloads'
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))


checkVideo("https://www.youtube.com/shorts/VsFtd-mGzus")
