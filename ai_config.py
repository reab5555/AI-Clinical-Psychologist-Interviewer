from io import BytesIO

from langchain_openai import ChatOpenAI
from openai import OpenAI
import tiktoken
import os

def n_of_questions():
    n_of_questions = 30
    return n_of_questions

#openai_api_key = os.environ.get("openai_api_key")
openai_api_key = 'your_openai_api_key'

model = "gpt-4o-mini"

def load_model(openai_api_key):
    return ChatOpenAI(
        model_name=model,
        openai_api_key=openai_api_key,
        temperature=0.3,
        top_p=0.8
    )

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=openai_api_key)


def convert_text_to_speech(text, output):
    try:
        # Convert the final text to speech
        response = client.audio.speech.create(model="tts-1", voice="alloy", input=text, speed=1.15)

        if isinstance(output, BytesIO):
            # If output is a BytesIO object, write directly to it
            for chunk in response.iter_bytes():
                output.write(chunk)
        else:
            # If output is a file path, open and write to it
            with open(output, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Fallback in case of error
        response = client.audio.speech.create(model="tts-1", voice="alloy", input='Here is my Report!')

        if isinstance(output, BytesIO):
            for chunk in response.iter_bytes():
                output.write(chunk)
        else:
            with open(output, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)


def transcribe_audio(audio):
    audio_file = open(audio, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcription.text