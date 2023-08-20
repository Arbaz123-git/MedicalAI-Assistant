import openai
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
from config import apikey


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

chatStr = ""


def chat(command):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User:{command}\n Medical AI: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside try and catch block
    talk(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response['choices'][0]["text"]


def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
           print("listening...")
           voice = listener.listen(source)
           print("Recognizing...")
           command = listener.recognize_google(voice)
           command = command.lower()
           if 'medical ai' in command:
               command = command.replace('medical ai', '')
               print(command)
    except:
        pass
    return command

def run_ma():
    command = take_command()
    print(command)

    if 'reset chat' in command:  # Check for "reset chat" command
        global user_conversation, ai_conversation
        user_conversation = ""
        ai_conversation = ""
        talk("Chat reset complete.")

    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is ' + time)

    elif 'date' in command:
        date = datetime.datetime.now().strftime('%d /%m /%y')
        print(date)
        talk('Todays date is' + date)

    elif 'tell me about' in command:
        info = command.replace('tell me about' , '')
        knowledge = wikipedia.summary(info, 2)
        print(knowledge)
        talk(knowledge)

    else:
        chat(command)

if __name__ == '__main__':
    print("PyCharm")
    talk("Hello, I am Medical AI")

user_conversation = ""  # Initialize empty strings to store the conversation
ai_conversation = ""

while True:
    run_ma()

    user_input = take_command()
    ai_response = chat(user_input)

    # Update the conversation strings
    user_conversation += f"User: {user_input}\n"
    ai_conversation += f"Medical AI: {ai_response}\n"

    # Print both the user's conversation and the AI's responses
    print(user_conversation)
    print(ai_conversation)



