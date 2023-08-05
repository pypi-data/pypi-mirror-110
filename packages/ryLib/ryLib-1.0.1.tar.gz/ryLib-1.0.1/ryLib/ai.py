from xes import AIspeak
def speak(text,sound='boy'):
    AIspeak.setmode(sound)
    AIspeak.speak(str(text))