import tkinter as tk
from threading import Thread
from speech_recognizer import SpeechRecognizer

class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Transcription App")
        self.setup_gui()
        self.speech_recognizer = SpeechRecognizer()
        self.recording_thread = None

    def setup_gui(self):
        self.label = tk.Label(self.master, text="Click 'Start Recording' to begin.", wraplength=300)
        self.label.pack()
        self.start_button = tk.Button(self.master, text="Start Recording", command=self.start_recording)
        self.start_button.pack()
        self.stop_button = tk.Button(self.master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.label.config(text="Recording...")
        self.recording_thread = Thread(target=self.speech_recognizer.recognize_stream, args=(self.update_label,))
        self.recording_thread.start()

    def stop_recording(self):
        self.speech_recognizer.stream_microphone().close()  # Needs proper implementation to safely stop the stream
        self.recording_thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.label.config(text="Stopped recording. Click 'Start Recording' to begin.")

    def update_label(self, text):
        if self.master:
            self.label.config(text=text)

# Set up the root window
if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
