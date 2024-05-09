from django.urls import path

from transcription.views import (
    CreateAudioView, 
    record_audio, 
    # sound_in_text,
    # search, 
    # trgm_search, 
    )

urlpatterns = [
    path('record-audio/', record_audio), # Стартовая страница, запуск микрафона
    path('api/create-audio/', CreateAudioView.as_view(), name='createaudio'), # Обработка audioBlob с микравона 
                                                                            # (rest api - подключена к кнопке StopRecording)
    # path('create_text/', sound_in_text), # Запуск нейронки vosk
    # path('search/', search), # Полнотекстовый поиск
    # path('trgm-search/', trgm_search), # Триграммный поиск
]

