#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import yaml
import ffmpeg
import whisper
import argparse

sys.path.append("./src/library")

from core.whisperanscript import Whisperancript

parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('--file-name', type=str, required=True)
parser.add_argument('--destination', type=str, required=True)
parser.add_argument('--model', default='base')
parser.add_argument("--language", type=str, default='en')
args = parser.parse_args()

if __name__ == '__main__':
	model = Whisperancript(args.file_name)
	if os.path.splitext(args.file_name)[-1] != '.wav':
		model.any2wav()

	result, raw_file_name = model.load_transcript(lang=args.language)
	model.print_lines(result)
	
	# pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token='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')
	# audio_file = args.wav_file_name
	# print(audio_file)
	# diarization = pipeline(audio_file, min_speakers=2, max_speakers=5)

	# audio = Audio(sample_rate=16000, mono=True)

	# for segment, _, speaker in diarization.itertracks(yield_label=True):
	#     waveform, sample_rate = audio.crop(audio_file, segment)
	#     text = model.transcribe(waveform.squeeze().numpy())["text"]
	#     print(f"[{segment.start:03.1f}s - {segment.end:03.1f}s] {speaker}: {text}")
	  