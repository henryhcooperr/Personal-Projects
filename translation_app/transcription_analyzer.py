import openai

class TranscriptionAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        # Set the API key for the openai module
        openai.api_key = self.api_key

    def analyze_transcription(self, text):
        """Post-process text using the new OpenAI API to refine or analyze the transcription."""
        try:
            response = self.client.chat.completions.create(
                model="text-davinci-002",  # Adjust the model as necessary
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Clarify this transcription: " + text}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred during analysis."

    def save_transcription(self, text, file_path='transcriptions.txt'):
        """Save the transcription to a file."""
        with open(file_path, "a") as file:
            file.write(text + '\n')
