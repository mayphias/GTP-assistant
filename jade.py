import openai
import pyttsx3
import speech_recognition as sr
import time

#setting open AI API key
openai.api_key = "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"

#inicialize the text-to-speech engine
engine = pyttsx3.init()

def get_device_index(recognizer):
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "mic" in name.lower():
            try:
                with sr.Microphone(device_index=index) as source:
                    p = recognizer.listen(source)
                    return index
            except sr.UnknownValueError:
                pass
    return None


def transcribe_audio_to_text (audio_input):
    recognizer = sr.Recognizer()
    device_index = get_device_index(recognizer)
    if device_index is None:
        print("No microphone found.")
        return
    with sr.Microphone(device_index=device_index) as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            print("Call jade!")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print("You said:", text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except:
                print("Skipping unknow error.")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response ["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
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
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phase_time_limit=None, timeout=None)
                        with open(audio_input, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    #transcribe the audio
                    text = transcribe_audio_to_text(audio_input)
                    if text:
                        print(f"You said: {text}")


                        #generate response using GTP-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        #read response using text-to-speech
                        speak_text(response)
            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()

