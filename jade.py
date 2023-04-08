import openai
import pyttsx3
import speech_recognition as sr
from contextlib import  contextmanager
from ctypes import *
import pyaudio
import time

#setting open AI API key
openai.api_key = "my-api-key"


#ALSA error handler
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

#texto em fala (fala inicial)
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

#inicialize the text-to-speech engine
engine = pyttsx3.init()

#setting up the output device to default "0"
pa = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
stream = pa.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 output=True,
                 output_device_index=0,
                 frames_per_buffer=CHUNK)

# Set the voice ID (use a different ID to change the voice)
voice_id = "kannada"
engine.setProperty("voice", voice_id)

#search for the microphone sony to utilize
def get_device_index(recognizer):
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #My specific mic
        if "Sony" in name:
            print("Mic found: ", name)
            return index
        #other mics
        if "mic" in name.lower():
            try:
                with sr.Microphone(device_index=index) as source:
                    p = recognizer.listen(source)
                    print("mic selected: ", p)
                    return index
            except sr.UnknownValueError:
                pass
    #if shown, error in picking up mic
    print("error no mic selected, here the list of devices: ", sr.Microphone.list_microphone_names())
    return None


def transcribe_audio_to_text(audio_input):
    recognizer = sr.Recognizer()
    device_index = get_device_index(recognizer)
    if device_index is None:
        print("No microphone found.")
        return None
    with sr.AudioFile(audio_input) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except:
        print("Skipping unknown error.")
        return None

def generate_response(prompt, additional_context=None):
    if additional_context:
        prompt = f"{additional_context}\n{prompt}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    # Say welcome message
    text_to_speech("Hi, my name is Jade. How can I assist you today?")

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        gdi = get_device_index(recognizer)
    while True:
        #wait for user to say "jade"
        print("Say 'jade' to start recording your question...")
        with sr.Microphone(device_index=gdi) as source:
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "jade":
                    #record audio
                    audio_input = "input.wav"
                    print("Say your question...")
                    with sr.Microphone(device_index=gdi) as source:
                        with noalsaerr():
                            source.pause_threshold = 1
                            audio = recognizer.listen(source, phase_time_limit=None, timeout=None)
                        with open(audio_input, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    #transcribe the audio
                    text = transcribe_audio_to_text(audio_input)
                    if text:
                        print(f"You said: {text}")

                        #generate response using GTP-3 with additional context
                        additional_context = "You are my assistant and my professor named jade, act like it."
                        response = generate_response(text, additional_context)
                        print(f"GPT-3 says: {response}")

                        #read response using text-to-speech
                        speak_text(response)
            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()

