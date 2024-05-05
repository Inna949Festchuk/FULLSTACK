from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from .serializers import AudioFileSerializer
from rest_framework.views import APIView
from transcription.models import Commands, UsersTexts
# Поисковый вектор, Выделение основ слов и ранжирование
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
# Поиск по триграммному сходству
from django.contrib.postgres.search import TrigramSimilarity

import os
import json
import subprocess
# import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

# - - - - - - - - - - - - - - - - - - - 
# Запускаем запись звука record_audio.html 
def record_audio(request):
    return render(request, 'record_audio.html')

# Эндпоинт для сохранения и постобработки audioBlob
class CreateAudioView(APIView):
    
    def post(self, request):
        serializer = AudioFileSerializer(data=request.FILES)
        if serializer.is_valid():
            audio_file = serializer.validated_data['audio']
            # Сохранение аудиофайла в папке media
            media_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
            audio_segment = AudioSegment.from_file(audio_file)
            audio_file_mp3 = audio_segment.export(media_path, format="mp3") # Поменять здесь и на фронте audioBlob, 
            # Выполняем функцию транскрибации
            convert_text = sound_in_text(audio_file_mp3) 
            # Выполняем функцию триграммного поиска соответствий в модели БД Commands 
            search_text = trgm_search(convert_text)  
            print(search_text)                                        
            return Response({'message': 'Аудиофайл успешно загружен'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Транскрибация
def sound_in_text(audio_file_mp3):
    '''
    По материалам "Решаем задачу перевода русской речи в текст с помощью Python и библиотеки Vosk" 
    https://proglib.io/p/reshaem-zadachu-perevoda-russkoy-rechi-v-tekst-s-pomoshchyu-python-i-biblioteki-vosk-2022-06-30
    (Дополнительно установить ffmpeg (менеджер pip не всегда срабатывает)
    при установке в конду использовать conda install -c conda-forge ffmpeg
    или скачать отдельно с сайта https://ffmpeg.org/download.html пакеты кодека ffmpeg
    Установите переменные среды с помощью путей к двоичным файлам FFmpeg:
    В Windows запустите:
    set FFMPEG_PATH=C:\path\to\ffmpeg.exe
    В Unix или MacOS запустите:
    export FFMPEG_PATH=/path/to/ffmpeg)
    Открытые модели для распознавания русской речи:
    https://alphacephei.com/nsh/2023/01/15/russian-models.html
    '''
    
    SetLogLevel(0)  # Логирование

    # Задаем путь к статике и медиа
    static_path = os.path.join(settings.STATICFILES_DIRS[0])
    media_path = os.path.join(settings.MEDIA_ROOT)

    # Проверяем наличие модели в текущей рабочей директории
    if not os.path.exists(static_path + "/speech/model"):
        print("Пожалуйста, загрузите модель с https://alphacephei.com/vosk/models и разархивируйте как 'model' в текущей папке.")
        # преждевременное завершение программы из-за отсутствия модели, необходимой для работы дальнейших инструкций.
        exit(1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    CHANNELS = 1

    model = Model(static_path + "/speech/model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    # Используя библиотеку pydub делаем предобработку аудио
    mp3 = AudioSegment.from_mp3(media_path + '/recorded_audio.mp3')
    mp3 = mp3.set_channels(CHANNELS)
    mp3 = mp3.set_frame_rate(FRAME_RATE)

    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    # Декодируем вывод строки json "{\n  \"text\" : \"\"\n}" в словарь Python
    text = json.loads(result)['text']
    # сохраняем в модель UsersTexts БД в поле usertext
    users_text = UsersTexts.objects.create(usertext=text) 
    users_text.save()

    # Сохраняем результат в файл JSON
    with open(static_path + '/speech/result.json', 'w', encoding='utf-8') as f:
        json.dump(text, f, ensure_ascii=False, indent=4)

    # Добавляем пунктуацию (требует наличия ядер CUDA)
    # cased = subprocess.check_output('python3 ./transcription/static/speech/recasepunc/recasepunc.py predict ./transcription/static/speech/recasepunc/checkpoint', shell=True, text=True, input=text)
    # with open(static_path + '/speech/data.txt', 'w') as f:
    #    json.dump(cased, f, ensure_ascii=False, indent=4)

    return text

# Поиск по триграммному сходству 
# (требует дополнительного расширения postgresql pg_trgm)
def trgm_search(query):
    '''
    Поиск по триграммному сходству
    Дополнительные настройки расширений postgresql:
    psql admin
    CREATE EXTENSION pg_trgm;
    ''' 
    searchresults = []
    searhfld = ['commands', 'confirmation']
    for allresult in searhfld:
        searchresults = Commands.objects.annotate(
                        similarity=TrigramSimilarity(allresult, query),
                        ).filter(similarity__gt=0.1).order_by('-similarity')
    out_query_set = [searchresult for searchresult in searchresults]
    if out_query_set == []:   
        return 'Извините я Вас не поняла, переключаю на оператора'
    
    return out_query_set[0] # ПЕРЕНАПРАВИТЬ НА МИКРОФОН

