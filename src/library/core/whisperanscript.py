#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import ffmpeg
import whisper

class Whisperancript:
	def __init__(self, filename, destination, model, logger):
		self.model       = model
		self.logger      = logger
		self.filename    = filename
		self.destination = destination
		os.makedirs(f"{self.destination}", exist_ok=True)

		self.wav_filename = f"{self.destination}/raw-audio.wav"
		self.yaml_filename = f"{self.destination}/whisper-result.yaml"
		self.txt_filename = f"{self.destination}/raw-transcript.txt"

	def any2wav(self):
		stream = ffmpeg.input(self.filename)
		stream = ffmpeg.output(stream, self.wav_filename)
		ffmpeg.run(stream)
		return self.wav_filename

	def load_transcript(self, lang = 'en'):
		raw_file_name = self.filename
		yaml_file_name = self.yaml_filename

		print('Now transcribing...')
		model = whisper.load_model(self.model)
		result = model.transcribe(self.wav_filename, verbose=False, language=lang)

		with open(yaml_file_name, 'w') as f:
			# yaml.dump(result, f, indent=4, allow_unicode=True, sort_keys=False)
			yaml.dump(result, f, indent=4, default_flow_style=False, allow_unicode=True, sort_keys=False)
		print('Finish transcribing...')
			
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
	
		