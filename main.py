import speech_recognition as sr
import win32com.client
import webbrowser
import os
import datetime
import openai
from config import apikey
import random
# from AppOpener import open
chatStr=" "
def chat(query):
    global chatStr
    openai.api_key =apikey
    chatStr=chatStr + f"Uday: {query}\n Jarvis:"

    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    speaker.Speak(response["choices"][0]["text"])
    chatStr=chatStr+f"{ response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]
    


def ai(prompt):
    openai.api_key =apikey
    text=f"OpenAI response for prompt: {prompt} \n*********\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response["choices"][0]["text"])
    text=text+ response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt","w") as f:
        f.write(text)



speaker = win32com.client.Dispatch("SAPI.SpVoice")


def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold =  0.6
        audio =r.listen(source)
        try:
            query=r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
        except Exception as e:
            return "Some Error Occured. Sorry from Jarvis"
        return query
    

if __name__=='__main__':
    
    speaker.Speak("Jarvis A.I")
    
    while True:
        print("Listening...")

        query=takeCommand()
        sites=[["youtube","https://youtube.com"],["wikipedia","https://wikipedia.com"],["google","https://google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])

            elif "Open Spotify".lower() in query.lower():
               os.system("spotify")

            elif "the time".lower() in query.lower():
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                speaker.Speak(f"The time is {hour} hour {min} minutes")

            elif "using intelligence".lower() in query.lower():
                ai(prompt=query)


            elif "Jarvis Quit".lower() in query.lower():
                exit()
            elif "reset chat".lower() in query.lower():
                chatStr=""


            else:
                print("Chatting...")
                chat(query)


                
        # speaker.Speak(query)
     

