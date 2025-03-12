import pyttsx3 as p
import speech_recognition as sr
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Define the Infow class
class Infow:
    def __init__(self):
        service = Service(ChromeDriverManager().install())  # Auto-downloads the correct driver
        self.driver = webdriver.Chrome(service=service)

    def get_info(self, query):
        self.driver.get(url="https://www.wikipedia.org/")
        search = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
        search.click()
        search.send_keys(query)
        enter = self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button')
        enter.click()
        time.sleep(60)  # Let the page load

# Voice Assistant Setup
engine = p.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech Recognition
r = sr.Recognizer()
speak("Hello sir, I am your voice assistant Bella. How are you?")

with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source, 1.2)
    print("Listening...")

    try:
        audio = r.listen(source)
        text = r.recognize_google(audio)
        print(text)
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        text = ""

# Check User's Response
if "what about you" in text.lower():
    speak("I am having a good day, sir.")
    speak("How can I help you?")

    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        print("Listening for your request...")

        try:
            audio = r.listen(source)
            text2 = r.recognize_google(audio)
            print(text2)
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
            text2 = ""

    if "information" in text2.lower():
        speak("You need information on which topic?")
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("Listening for the topic...")

            try:
                audio = r.listen(source)
                infor = r.recognize_google(audio)
                print(f"Searching for: {infor}")
                speak(f"Searching {infor} in Wikipedia.")

                # Now Infow is properly defined
                assist = Infow()
                assist.get_info(infor)
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand the topic.")
