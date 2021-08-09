import speech_recognition as sr
import playsound
from gtts import gTTS, lang
import random
import os
import Dictionary

Recognizer = sr.Recognizer()

def Speak(text):
    #Synthezice assistant voice
    if text != None:
        tts = gTTS(text=text, lang="en")
        filename = (str(random.random()) + ".mp3")
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)

def Recognize():
    #Get voice input, turn it to text using google AI, and pass it to analyzer function to then get a response from Assistant
    with sr.Microphone() as source:
        try:
            audio = Recognizer.listen(source)
            text = Recognizer.recognize_google(audio).lower()       
            print(text)
            return text

        except:
            pass
