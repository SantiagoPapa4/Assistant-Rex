import Voice
import Dictionary
import os
import queue
import random
from threading import Thread
import clientTemp

Mode = ""
greetingPhrases = ["Welcome, sir. What mode will I be in?", "Welcome back! You now the drill", "Hello there, what mode?", "Long time no see, how will I work today?"] 
def init():
    global Mode
    Voice.Speak(greetingPhrases[random.randrange(len(greetingPhrases))])
    while True:
        answer = Voice.Recognize()
        if answer != None:
            if "silent" in answer:
                Mode = "silent"
                Voice.Speak("I will try to be quiet.")
                break
            if "offline" in answer:
                Voice.Speak("See you later")
                os.system("exit")
                break
            if  "interactive" in answer:
                Mode = "interactive"
                Voice.Speak("I'm here for whatever you need")
                break

if __name__ == "__main__":
    init()
    print("Initializing in {} mode.".format(Mode))
    #Constantly recognize voice
    while True:
        phrase = Voice.Recognize()
        answer = clientTemp.communicate(phrase)
        if answer != "":
            Voice.Speak(answer)
