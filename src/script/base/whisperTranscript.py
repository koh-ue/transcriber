#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import ffmpeg
import whisper
import argparse
#from pyannote.audio import Audio
#from pyannote.audio import Pipeline


parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-f', '--file_name', type=str, default='')
parser.add_argument('-m', '--model', choices=['tiny', 'base', 'small', 'medium', 'large'], default='base')

args = parser.parse_args()

class Whisperancript:
	def __init__(self, file_name):
		self.filename = file_name
		self.basename = os.path.splitext(os.path.basename(self.filename))[0] # USAGE: /sample/test.mov --> test
		os.makedirs(f"../result/{self.basename}", exist_ok=True)

		self.wav_filename = f"../result/{self.basename}/{self.basename}.wav"
		self.json_filename = f"../result/{self.basename}/{self.basename}.json"
		self.txt_filename = f"../result/{self.basename}/{self.basename}.txt"

	def any2wav(self):
		stream = ffmpeg.input(self.filename)
		stream = ffmpeg.output(stream, self.wav_filename)
		ffmpeg.run(stream)
		return self.wav_filename



	def load_transcript(self, lang = 'en'):
		raw_file_name = self.filename
		json_file_name = self.json_filename

		if not os.path.isfile(json_file_name):
			print('Now transcribing...')
			model = whisper.load_model(args.model)
			result = model.transcribe(self.wav_filename, verbose=False, language=lang)

			with open(json_file_name, 'w') as f:
				json.dump(result, f, indent=4)
			print('Finish transcribing...')
		else:
			print(json_file_name + " already exsits.")
			with open(json_file_name, 'r') as f:
				result = json.load(f)
			
		#print(result['text'])
		return result, raw_file_name

	def print_lines(self, json_dictionary):
		txt_file_name = self.txt_filename
		
		print('Now printing...')
		f = open(txt_file_name, 'w')
		for i in range(len(json_dictionary['segments'])):
			item = json_dictionary['segments'][i]['text']
			print(item)
			f.writelines(item + '\n\n')
		f.close()
		print('Finish printing...')
	
		

if __name__ == '__main__':
	model = Whisperancript(args.file_name)
	model.any2wav()

	result, raw_file_name = model.load_transcript(lang='en')
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
	  