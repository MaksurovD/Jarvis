import sounddevice as sd
import torch
import time
#Настраиваемые параметры
#Виды операторов озвучки aidar, baya, kseniya, xenia, eugene

class Voice:
    #Виды операторов озвучки aidar, baya, kseniya, xenia, eugene
    def __init__(self,speaker='eugene'):
        self.language = 'ru'
        self.model_id = 'v3_1_ru'
        self.sample_rate = 48000
        self.speaker = speaker
        self.device = torch.device('cpu')

        self.model,text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                model='silero_tts',
                                language=self.language,
                                speaker=self.model_id)
        self.model.to(self.device) # gpu or cpu

    def say(self, text):
        audio = self.model.apply_tts(text=text,
                        speaker=self.speaker,
                        sample_rate=self.sample_rate)

        sd.play(audio,self.sample_rate)
        time.sleep(len(audio) / (self.sample_rate))
        sd.stop()