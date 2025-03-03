import speech_recognition as sr
import pyttsx3
import datetime
import os
import subprocess
import webbrowser
import wikipedia
from pathlib import Path

class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Set voice properties
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Index 0 for male, 1 for female
        self.engine.setProperty('rate', 150)  # Speed of speech
        
        # Configure Wikipedia
        wikipedia.set_lang('en')
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Alice: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for user input through microphone"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
            
        try:
            print("Recognizing...")
            command = self.recognizer.recognize_google(audio, language='en-US')
            print(f"User: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return ""
        except sr.RequestError:
            self.speak("Sorry, there was an error with the speech recognition service.")
            return ""
    
    def search_wikipedia(self, query):
        """Search Wikipedia and return summary"""
        try:
            # Remove the "wikipedia" keyword from the query
            search_query = query.replace("wikipedia", "").strip()
            
            # Get summary from Wikipedia
            self.speak(f"Searching Wikipedia for {search_query}...")
            result = wikipedia.summary(search_query, sentences=3)
            self.speak("According to Wikipedia...")
            self.speak(result)
            
            # Get the full page URL
            page = wikipedia.page(search_query)
            webbrowser.open(page.url)
            self.speak("I've opened the full article in your browser.")
            
        except wikipedia.DisambiguationError as e:
            self.speak("There are multiple matches. Please be more specific.")
            options = e.options[:5]  # Get first 5 options
            self.speak("Some possible matches are: " + ", ".join(options))
            
        except wikipedia.PageError:
            self.speak("Sorry, I couldn't find any Wikipedia article matching your query.")
            
        except Exception as e:
            self.speak("Sorry, there was an error while searching Wikipedia.")
            
    def process_command(self, command):
        """Process user commands and execute appropriate actions"""
        if "hello" in command or "hi" in command:
            self.speak("Hello! How can I help you today?")
            
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            
        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today's date is {current_date}")
            
        elif "open" in command:
            if "notepad" in command:
                subprocess.Popen("notepad.exe")
                self.speak("Opening Notepad")
            elif "calculator" in command:
                subprocess.Popen("calc.exe")
                self.speak("Opening Calculator")
                
        elif "search" in command:
            search_term = command.replace("search", "").strip()
            if search_term:
                url = f"https://www.google.com/search?q={search_term}"
                webbrowser.open(url)
                self.speak(f"Searching for {search_term}")
                
        elif "wikipedia" in command:
            self.search_wikipedia(command)
                
        elif "exit" in command or "quit" in command or "goodbye" in command:
            self.speak("Goodbye! Have a great day!")
            return False
            
        return True

def main():
    # Create voice assistant instance
    assistant = VoiceAssistant()
    assistant.speak("Hello! I'm your voice assistant. How can I help you?")
    
    running = True
    while running:
        command = assistant.listen()
        if command:
            running = assistant.process_command(command)

if __name__ == "__main__":
    main()