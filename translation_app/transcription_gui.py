import tkinter as tk
from threading import Thread
from speech_recognizer import SpeechRecognizer
import speech_recognition as sr

class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Transcription App")
        self.state = False
        self.setup_gui()
        self.speech_recognizer = SpeechRecognizer()

    def setup_gui(self):
        self.label = tk.Label(self.master, text="Click 'Start Recording' to begin.", wraplength=300)
        self.label.pack()
        self.start_button = tk.Button(self.master, text="Start Recording", command=self.start_recording)
        self.start_button.pack()
        self.stop_button = tk.Button(self.master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

    def start_recording(self):
        self.state = True
        self.label.config(text="Recording...")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.thread = Thread(target=self.record)
        self.thread.start()

    def stop_recording(self):
        self.state = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.label.config(text="Stopped recording. Click 'Start Recording' to begin.")

    def record(self):
        with sr.Microphone() as source:
            while self.state:
                text = self.speech_recognizer.recognize_speech(source)
                if text is not None:
                    self.update_label(text)

    def update_label(self, text):
        if self.state:
            self.label.config(text=text)
            print(text)
