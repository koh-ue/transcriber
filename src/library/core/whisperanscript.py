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

		self.wav_filename = f"{self.destination}/raw.wav"
		self.yaml_filename = f"{self.destination}/result.yaml"

		self.logger.info(f"target: {self.filename}")
		self.any2wav()

	def any2wav(self):
		stream = ffmpeg.input(self.filename)
		stream = ffmpeg.output(stream, self.wav_filename)
		ffmpeg.run(stream)
		return self.wav_filename

	def transcribe(self, lang = 'en'):
		raw_file_name = self.filename
		yaml_file_name = self.yaml_filename

		self.logger.info('Now transcribing...')
		model = whisper.load_model(self.model)
		result = model.transcribe(audio=self.wav_filename, verbose=False, language=lang)

		with open(yaml_file_name, 'w') as f:
			yaml.dump(result, f, indent=4, default_flow_style=False, allow_unicode=True, sort_keys=False)
		self.logger.info('Finish transcribing...')
		
		return result, raw_file_name
	
		