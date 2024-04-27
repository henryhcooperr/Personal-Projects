import pyaudio
from google.cloud import speech

class SpeechRecognizer:
    def __init__(self):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True
        )

    def stream_microphone(self):
        """Generator that yields audio chunks from the microphone."""
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)
        try:
            while True:
                yield stream.read(1024)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def recognize_stream(self):
        """Recognize speech from the microphone stream."""
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in self.stream_microphone())
        responses = self.client.streaming_recognize(self.streaming_config, requests)

        for response in responses:
            for result in response.results:
                if result.is_final:
                    print('Final transcript:', result.alternatives[0].transcript)
                else:
                    print('Interim result:', result.alternatives[0].transcript)

# Example usage
if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    recognizer.recognize_stream()
