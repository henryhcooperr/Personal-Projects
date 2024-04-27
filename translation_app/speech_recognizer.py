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
        self.audio_stream = None
        self.keep_recording = True

    def stream_microphone(self):
        p = pyaudio.PyAudio()
        self.audio_stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        try:
            while self.keep_recording:
                yield self.audio_stream.read(1024)
        finally:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            p.terminate()

    def recognize_stream(self, update_callback):
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in self.stream_microphone())
        responses = self.client.streaming_recognize(self.streaming_config, requests)
        for response in responses:
            for result in response.results:
                update_callback(result.alternatives[0].transcript)

    def stop(self):
        self.keep_recording = False
