from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os
import webbrowser
import random
import datetime
from num2words import num2words
from p1zdabol import Voice


def SoundDown():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(max(volume.GetMasterVolumeLevel()-5,-37), None)

def SoundUp():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(min(volume.GetMasterVolumeLevel() + 5, 0), None)

def SoundOff():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(True, None)

def SoundOn():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(False, None)


def StartYoutube():
    webbrowser.open("https://www.youtube.com/")

def StartBrowser():
    webbrowser.open("https://www.google.ru/?hl=ru")

def StartYoutubeMusic():
    webbrowser.open("https://music.youtube.com/browse/UCo-9IeMlglEWkpB9mOcH7pg")

def StartMusicForJob():
    webbrowser.open("https://www.youtube.com/watch?v=jfKfPfyJRdk")

def StartMusicForRelax():
    webbrowser.open("https://www.youtube.com/watch?v=MVPTGNGiI-4")

def StartMusicForSleep():
    webbrowser.open("https://www.youtube.com/watch?v=rUxyKA_-grg")

def TimeNow():
    now = datetime.datetime.now()
    current_time = now.strftime("%H %M %S")
    hour = num2words(int(current_time.split()[0]), lang='ru')
    min = num2words(int(current_time.split()[1]), lang='ru')
    voice = Voice()
    voice.say(f"Текущее время: {hour} часов {min} минут")
    print(f"Текущее время: {hour} часов {min} минут")

def Command_Execution_mode(self):
    self.AnswerMode = "Command Execution mode"
    self.VoiceOverApi.say("Режим выполнения команд активирован")

def Сonversational_mode(self):
    self.AnswerMode = "Сonversational mode"
    self.VoiceOverApi.say("Разговорный режим включён")

def Intermediate_mode(self):
    self.AnswerMode = "Intermediate mode"
    self.VoiceOverApi.say("Промежуточный режим активирован")
