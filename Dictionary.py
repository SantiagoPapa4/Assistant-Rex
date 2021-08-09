import os
import sys
import ctypes
import datetime
from googlesearch import search
from subprocess import call
import webbrowser
import Voice

def Translate(stt, mode):

    if stt == None:
        return None
    text = ""
    if mode == "silent" and not "echo" in stt:
        return None
    if mode == "silent" and "echo" in stt:
        text = str(stt).replace("echo", "")
    if mode == "interactive":
        text = stt
    if mode == "offline":
        return None  

### Priority 

    if "search for" in text:
        print( text.split("search for ")[1].replace(" ", "+") )
        #call(["gnome-terminal -e opera https://www.google.com/search?q={}".format(text.split("search for ")[1].replace(" ", "+"))], shell=True)
        webbrowser.open("https://www.google.com/search?q={}".format(text.split("search for ")[1].replace(" ", "+")))

### Basic Stuff
    if "what time is it" in text or "what's the time" in text:
        print(datetime.datetime.now().strftime("%H %M"))
        return(str(datetime.datetime.now().strftime("%H %M")))
    if "thank" in text:
        return("You are welcome")
    if "shut yourself down" in text:
        Voice.Speak("See ya!")
        os.system("exit")
        os.system("exit")
        os.system("exit")
    if "take a screenshot" in text:
        call(['gnome-terminal -e gnome-screenshot -i'], shell=True)

### Player Commands
    if "turn the volume up" in text or "volume up" in text:
        call(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
        return("Sure, its up")        
    if "turn the volume down" in text or "volume down" in text:
        call(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
        return("Turning it down")
    if "stop the player" in text or text == "pause":
        call(["playerctl", "pause"])
        return("Right away")
    if "continue playing" in text or text == "continue":
        call(["playerctl", "play"])
        return("Right away") 

### Application Control
    if "open the application" in text:
        appname = text.split("open the application ")[1]
        call(['gnome-terminal -e  {}'.format(appname)], shell=True)

    if "close the application" in text:
        #TODO
        pass

### File Transfer

    if text == "upload a file" or text == "upload":
        pass
    if text == "download a file" or text == "download":
        pass

### Remote Desktop

###JarvisNet