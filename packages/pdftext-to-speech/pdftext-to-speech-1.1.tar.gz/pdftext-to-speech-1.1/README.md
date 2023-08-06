# Text To Speech

The TextToSpeech project is a Python-based application that enables users to convert PDF and TXT files into audio files in the WAV format. With this project, users can easily transform written text into spoken words, making it convenient for individuals who prefer listening over reading. The project utilizes the PyPDF2 library to extract text from PDF files and supports direct text input from TXT files. Users can specify the desired language and pass the text to a Text-to-Speech API, which generates the corresponding audio data. The final output is saved as an audio file in WAV format, providing a seamless experience for anyone looking to convert written content into an audio format.

## Installation

You can install TicTacToeEnhanced using pip:

```shell
pip install pdftext-to-speech
```
 
# Usage


```python
from textToSpeech.textToSpeech import Audio, AudioRequest, File

# you can use any other API, I am using text to speech from rapidapi
url = "https://text-to-speech27.p.rapidapi.com/speech"

# define your filename and working directory
# define working directory (the directory where the file resides). Keep empty to get the file from the same working directory
my_file = File('sample.pdf', working_dir='speeches')

# text response is a dict with the text inside txt
text = my_file.read_file()["txt"]

# make sure to define your language
# for a full list check languages.txt in the git repo
querystring = {"text":text,"lang":"en-us"}

# particular for this API. Use your own
headers = {
	"X-RapidAPI-Key": "YOUR API KEY",
	"X-RapidAPI-Host": "text-to-speech27.p.rapidapi.com"
}

audio_request = AudioRequest(url=url, querystring=querystring, headers=headers)
response = audio_request.request_audio_data()

# name your file what you want, my api return bytes convertable to wav
# you can change your output directory or keep it empty so the file is saved same as your working directory
audio = Audio(audio_filename="speech.wav", output_directory="speeches")

result = audio.save_audio_file(response)

print(result["message"])
```

# Enjoy :)

# Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on [GitHub](https://github.com/danysrour/textToSpeech).

# License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/danysrour/textToSpeech/master/LICENSE.txt)

```text

You can now copy this code and use it as your README.md file.
```