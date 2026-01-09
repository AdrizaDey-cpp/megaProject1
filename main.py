import speech_recognition as sr
import os
import pyttsx3
import requests
import webbrowser
import time

#speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 180) #to adjust speed

newsapi = "enter your api key here"

def speak(text):
    print(f"Momo: {text}")
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower()
    print(f"--- Processing: '{c}' ---")
    
    if "google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        
    elif "facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "youtube" in c:
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")

    elif "timeless song" in c:
        speak("playing timeless") in c:
        webbrowser.open("https://youtu.be/5EpyN_6dqyk?si=KaR_zlT5x_AXbKWs")
        
    elif "news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            data = r.json()
            articles = data.get('articles', [])
            speak("Here are the top headlines.")
            for article in articles[:2]: 
                speak(article['title'])
        except Exception:
            speak("Sorry, I can't get the news right now.")
    
    else:
        speak("I'm not sure how to do that yet.")

if __name__ == "__main__":
    speak("Momo is active now.")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("\nListening for 'Momo'...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
            
            full_text = recognizer.recognize_google(audio).lower()
            print(f"Heard: {full_text}")
            
            if "momo" in full_text:
                # Check if there is a command after the word "momo"
                command = full_text.split("momo")[-1].strip()
                
                if command:
                    processCommand(command)
                else:
                    # If user just said "Momo", ask what they want
                    speak("How can I help you?")
                    with sr.Microphone() as source:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)

        except sr.UnknownValueError:
            # This ignores background noise that isn't speech
            pass
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"Error: {e}")