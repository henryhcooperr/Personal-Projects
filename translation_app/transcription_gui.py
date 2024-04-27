import tkinter as tk
from tkinter import ttk  # Themed Tkinter for better looking widgets
from threading import Thread
from speech_recognizer import SpeechRecognizer
from transcription_analyzer import TranscriptionAnalyzer
import os



class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Transcription App")
        self.main_frame = ttk.Frame(master, padding="10 10 10 10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.setup_gui()
        self.speech_recognizer = SpeechRecognizer()
        self.recording_thread = None
        # Initialize the analyzer with your OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        print("Retrieved API Key:", api_key)  # This should print your actual API key, ensure it's correct and not None or 'api_key'

        if not api_key:
            raise ValueError("API key is not set")
        self.analyzer = TranscriptionAnalyzer(api_key)

    def setup_gui(self):
        # Configuring the layout with ttk for a consistent look
        self.label = ttk.Label(self.main_frame, text="Click 'Start Recording' to begin.", wraplength=300)
        self.label.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.start_button = ttk.Button(self.main_frame, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=1, column=0, sticky=tk.W)

        self.stop_button = ttk.Button(self.main_frame, text="Stop Recording", command=self.stop_recording, state='disabled')
        self.stop_button.grid(row=1, column=1, sticky=tk.E)

        # Adding a scrolling text area for transcripts
        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.text = tk.Text(self.text_frame, height=10, width=50)
        self.text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text['yscrollcommand'] = scrollbar.set

        # Set style for better aesthetics
        style = ttk.Style()
        style.theme_use('clam')  # Try 'alt', 'default', 'classic', 'vista'

        # Responsive design
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.rowconfigure(0, weight=1)

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)  # Disable the start button
        self.stop_button.config(state=tk.NORMAL)  # Enable the stop button
        self.label.config(text="Recording...")  # Update the label to indicate recording
        # Ensure that we start the recognition process in a non-blocking way
        self.recording_thread = Thread(target=self.speech_recognizer.recognize_stream, args=(self.update_label,))
        self.recording_thread.start()  # Start the thread

    def stop_recording(self):
        self.speech_recognizer.stop()  # Properly stop the recording
        if self.recording_thread.is_alive():
            self.recording_thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.label.config(text="Stopped recording. Click 'Start Recording' to begin.")

    def update_label(self, text, is_final=False):
        if is_final:
            self.text.insert(tk.END, text + '\n')
            self.text.see(tk.END)
            analyzed_text = self.analyzer.analyze_transcription(text)
            print(analyzed_text)  # Optionally display or further process the analyzed text
            self.analyzer.save_transcription(text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
