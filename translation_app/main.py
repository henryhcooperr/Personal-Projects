import tkinter as tk
from transcription_gui import TranscriptionApp

def main():
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
