# Jade - AI Personal Assistant

Jade is an AI personal assistant built using OpenAI's GPT-3.5 architecture. It can perform a variety of tasks such as answering questions, making recommendations, and helping with day-to-day tasks.

## Getting Started

To get started, clone this repository onto your local machine:

``` bash
git clone https://github.com/mayphias/GTP-assistant
```

Once you have cloned the repository, you will need to install the required Python packages:

``` bash
pip install openai
pip install pyaudio
pip install speech_recognition
```

Next, you will need to set up your OpenAI API key. You can do this by creating a free account at OpenAI and generating an API key. Once you have your API key, you can set it as an environment variable in the python jade.py file ("openai.api_key").

## Known Issues

- When testing on a Linux machine, we encountered a `malloc()` error with our ALSA driver code, which prevented us from fully testing the audio functionality. We are actively working on resolving this issue and appreciate your patience.


## Contributions

Contributions to Jade are welcome! If you find a bug or have an idea for a new feature, feel free to open an issue or submit a pull request. This program was made inspired from the youtube video from the [Ai Austin](https://www.youtube.com/watch?v=8z8Cobsvc9k&ab_channel=AiAustin):

## Lincense

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This project was inspired by other AI personal assistants such as Siri and Alexa. Special thanks to OpenAI for providing the GPT-3.5 architecture.

tags: #python, #opensource, #begginer-friendly, #api