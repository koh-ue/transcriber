#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import whisper
import argparse
#from pyannote.audio import Audio
#from pyannote.audio import Pipeline


parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-w', '--wav_file_name', type=str, default='')
parser.add_argument('-m', '--model', choices=['tiny', 'base', 'small', 'medium', 'large'], default='base')

args = parser.parse_args()


def load_transcript(wav_file_name):
	raw_file_name = os.path.splitext(wav_file_name)[0]
	json_file_name = f'{raw_file_name}.json'

	if not os.path.isfile(json_file_name):
		print('Now transcribing...')
		model = whisper.load_model(args.model)
		result = model.transcribe(wav_file_name, verbose=False)

		with open(json_file_name, 'w') as f:
			json.dump(result, f, indent=4)
		print('Finish transcribing...')
	else:
		print(json_file_name + " already exsits.")
		with open(json_file_name, 'r') as f:
			result = json.load(f)
		
	#print(result['text'])
	return result, raw_file_name

def print_lines(json_dictionary, raw_file_name):
	txt_file_name = f'{raw_file_name}.txt'
	
	print('Now printing...')
	f = open(txt_file_name, 'w')
	for i in range(len(json_dictionary['segments'])):
		item = json_dictionary['segments'][i]['text']
		print(item)
		f.writelines(item + '\n\n')
	f.close()
	print('Finish printing...')
	
		

if __name__ == '__main__':
	result, raw_file_name = load_transcript(args.wav_file_name)
	print_lines(result, raw_file_name)
	"""
	pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token='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')
	audio_file = args.wav_file_name
	print(audio_file)
	diarization = pipeline(audio_file, min_speakers=2, max_speakers=5)

	audio = Audio(sample_rate=16000, mono=True)

	for segment, _, speaker in diarization.itertracks(yield_label=True):
	    waveform, sample_rate = audio.crop(audio_file, segment)
	    text = model.transcribe(waveform.squeeze().numpy())["text"]
	    print(f"[{segment.start:03.1f}s - {segment.end:03.1f}s] {speaker}: {text}")
	  """