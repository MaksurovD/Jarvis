import queue
import sounddevice as sd
import vosk
import json
from words import *
from p1zdabol import Voice
from AI import AIAPI
from func import *


#Настраиваемые параметры
#Виды модели распознования "vosk-model-ru-0.42" 'vosk_model'


#Интерфейс распознования речи
class Recognizer:
    #Виды операторов озвучки aidar, baya, kseniya, xenia, eugene
    def __init__(self,ActiveMode ='Quick Response mode',AnswerMode = "Intermediate mode", speaker = 'eugene',modelFile = 'vosk_model',model='davinci_003'):
        self.__SongActiveFlag = True
        self.__ActiveMode = ActiveMode
        self.AnswerMode = AnswerMode

        self.__q = queue.Queue()

        self.__model = vosk.Model(modelFile)  # Определение языковой модели (Модель находится в папке vosk_model)
        self.__device = sd.default.device  # Сохранение номеров портов ввода и вывода, переменная Device равна [1,4] первый порт микрофона, второй порт динамика
        self.__samplerate = int(sd.query_devices(self.__device[0], 'input')['default_samplerate'])  # Сохранение параметров микрофона


        #Настройка главного мозга
        self.VoiceOverApi = Voice(speaker) #Подключение API Озвучки, параметр speaker опруделяет оператора

        self.__ResponceAPI = AIAPI(model) #Подключение API ИИ для формирования ответа



    # Функция обработки формирования последовательности из распознанных слов
    def __callback(self, indata, frames, time, status):
        if (self.__SongActiveFlag):
            self.__q.put(bytes(indata))


    # Функция создания и озвучивания ответа
    def __vocalizeAnswer(self, data):
        if data:
            self.__SongActiveFlag = False  # ограничение по распознованию во время озвучки
            if self.AnswerMode == "Intermediate mode":
                if ((len(data.split()) < 10)and(Action_trigger.intersection(data.split()))):
                    answer = self.__ResponceAPI.response(data)
                    print(answer)
                    exec(answer)
                else:
                    answer = self.__ResponceAPI.responseGPT(data)
                    print(answer)
                    try:
                        self.VoiceOverApi.say(answer)
                    except Exception:
                        print("")

            elif self.AnswerMode == "Сonversational mode":
                if self.__ResponceAPI.response(data) in ["Intermediate_mode(self)","Command_Execution_mode(self)"]:
                    exec(self.__ResponceAPI.response(data))
                else:
                    answer = self.__ResponceAPI.responseGPT(data)
                    print(answer)
                    try:
                        self.VoiceOverApi.say(answer)
                    except Exception:
                        print("")

            elif self.AnswerMode == "Command Execution mode":
                answer = self.__ResponceAPI.response(data)
                print(answer)
                exec(answer)
            self.__SongActiveFlag = True  # отключение ограничения по распознованию во время озвучки


    # Распознование речи
    def recognition(self):
        with sd.RawInputStream(samplerate=self.__samplerate, blocksize=8000, device=self.__device[0], dtype="int16",
                               channels=1,
                               callback=self.__callback):
            rec = vosk.KaldiRecognizer(self.__model, self.__samplerate)
            while True:
                data = self.__q.get()
                if rec.AcceptWaveform(data):
                    data = json.loads(rec.FinalResult())['text']
                    print(data)

                    if self.__ActiveMode == "Quick Response mode":
                        self.__vocalizeAnswer(data)
                        break
                    elif self.__ActiveMode == "Long talk mode":
                        if SleepTrigger.intersection(data.split()) and data.split()[0] == Trigger:
                            break
                        else:
                            self.__vocalizeAnswer(data)

                else:
                    print(rec.PartialResult())
