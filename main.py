# Перед запуском установить
# sounddevice
# scikit-learn
# vosk
# silero
# pvporcupine (Pico Voice)
import pvporcupine
from Recognizer import Recognizer
from pvrecorder import PvRecorder
import words


#Настраиваемые параметры
#Виды операторов озвучки aidar, baya, kseniya, xenia, eugene
#Виды модели распознования "vosk-model-ru-0.42" 'vosk_model'
#Виды моделей формирования ответов 'davinci_003', "GPT3_5Turbo"
#Виды ружимов активации "Quick Response mode" "Long talk mode"
#Виды режимов разговора "Intermediate mode", "Сonversational mode", "Command Execution mode"

porcupine = pvporcupine.create(
    access_key=words.APIKeyPicoVoice,
    keywords=["jarvis"],
    sensitivities=[1]
)
#Функция распознования речи и тренировки модели на исходном датасете
def main():
   Jarvis = Recognizer()
   recorder = PvRecorder(device_index=0, frame_length=porcupine.frame_length)
   recorder.start()
   while True:
       pcm = recorder.read()
       keyword_index = porcupine.process(pcm)
       if keyword_index >=0:
           recorder.stop()
           Jarvis.recognition()
           recorder.start()

if __name__ == '__main__':
    main()
