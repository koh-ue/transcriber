# TRANSCRIBER

## Overview
Transcriber offers tools to transcribe any audio and videos into text. Mainly, this repo uses [Whisper](https://openai.com/research/whisper). Previously, this project also used [Google Speech-to-Text](https://cloud.google.com/speech-to-text), However, models woth Whisper seem to be superior to ones with Google Speech-to-Text. These codes about Speech-to-Text are in `src/legacy`

## Installation

Confirmed environment is:
- Ubuntu 22.04.3
- Homebrew 4.1.12
- pyenv 2.3.27
- miniconda3-3.11-23.5.2-0
- **Python 3.11.4**
  
All requirements are in `requirements.txt`. Please install by executing:
```sh
pip install -r requirements.txt
```

## Minimum Use

Main file is `src/script/base/whisperTranscript.py`. Including this file, ***all files are supposed to be executed from the root directories***.Available basic multilingual whisper models are `['tiny', 'base', 'small', 'medium', 'large']`. There are other models. Detailed description is [here](https://github.com/openai/whisper#available-models-and-languages). Languages' description is also provided in the same page. Language keywords to put as an argument are [here](https://github.com/openai/whisper/blob/0a60fcaa9b86748389a656aa013c416030287d47/whisper/tokenizer.py#L10)

You can transcribe any audio or videos by:
```sh
python src/script/base/whisperTranscript.py --file-name <YOUR_FILE_PATH> --model base --language en
```

For example:
```sh
python src/script/base/whisperTranscript.py --file-name ../examples/sample.mp4 --model base --language en
```

In this program, any audio files or movie files will be converted to .wav files before transcription.

