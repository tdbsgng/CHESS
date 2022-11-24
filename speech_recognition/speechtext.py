import speech_recognition as sr
import Levenshtein as lv
from difflib import SequenceMatcher
import requests

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def listen():
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio)
            print("Recognized text:", text)
            result = checkValidCommands(text)
            print("Analyzed text:", result)
    except sr.UnknownValueError():
        recognizer = sr.Recognizer()

def checkValidCommands(text):
    # Valid commands
    piece = ['car', 'horse', 'elephant', 'general', 'king', 'canon', 'soldier']
    position = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    # Separate commands
    curr_piece, curr_pos = text.split()
    curr_piece = curr_piece.lower()
    curr_pos = curr_pos.lower()
    x = curr_pos[-1]
    y = curr_pos[:-1]
    # Analyze which piece
    if curr_piece not in piece:
        temp = -1.0
        index = 0
        for i in range(len(piece)):
            jaro  = lv.jaro_winkler(curr_piece, piece[i])
            if temp <= jaro:
                index = i
                temp = jaro
        curr_piece = piece[index]
    # Analyze which y position
    if y not in position:
        temp = -1.0
        index = 0
        for i in range(len(position)):
            jaro = lv.jaro_winkler(y, position[i])
            if temp <= jaro:
                index = i
                temp = jaro
        y = position[index]
    # Analyze which x position
    try:
        temp = int(x)
        if temp > 9:
            x = 9
        else:
            x = temp
    except:
        x = 9
    # Result
    res = "{0} {1}{2}".format(curr_piece, y, x)
    return res

def record(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    print("Recognized text:", text)
    result = checkValidCommands(text)
    print("Analyzed text:", result)
    return result

if __name__ == "__main__":
    # Listen
    text = record("J8.wav")
    # JSONify
    text = text.split()
    piece = text[0]
    x = text[1][1]
    y = text[1][0]
    jsonfile = {
        "piece": piece,
        "x": x,
        "y": y
    }
    # POST request
    res = requests.post("http://localhost:5000/listen/send", json=jsonfile)
    if res.ok:
        print(res.json)
    