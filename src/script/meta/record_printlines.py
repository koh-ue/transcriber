#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import wave
import json
import whisper
import pyaudio
import argparse
import datetime
import subprocess
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-d', '--debug', action='store_true', help="shows commands to be run.")
parser.add_argument('-a', '--action', type=str, choices=['get_mic', 'record_transcribe', 'read', 'play', 'transcribe'], default='record_transcribe',\
					help='get_mic->shows a microphone list. record_transcribe->records an audio and transcribe it. read->shows waves and FFT of an audio file. play->plays an audio file. transcribe->transcribes an audio file into a text file.')
parser.add_argument('-c', '--channel', type=int, default=0, help='CHANNEL must be from channel index from --debug.')
parser.add_argument('-r', '--recording_time', type=str, default='0-0-5', help='RECOEDING_TIME should be [HOURS]-[MINUTES]-[SECONDS].')
parser.add_argument('-w', '--wav_file_name', type=str, default='OUTPUT_FILE', help='WAV_FILE_NAME is for transcribe, read, and play.')
parser.add_argument('-m', '--model', choices=['tiny', 'base', 'small', 'medium', 'large'], default='base')


args = parser.parse_args()

if __name__ == "__main__":
	cmd = 'python src/script/base/record.py'
	cmd_2 = 'python src/script/base/transcript.py'
	if args.action == 'get_mic':
		cmd += ' --debug'
		print('[0] ' + cmd)
		if not args.debug:
			subprocess.run(cmd.split())
		sys.exit()

	elif args.action == 'record_transcribe':
		cmd += f' --channel {args.channel}'
		cmd += f' --action record'
		cmd += f' --recording_time {args.recording_time}'
		cmd_2 += f' --model {args.model}'
		print('[0] ' + cmd)

		if not args.debug:
			try:
				subprocess.run(cmd.split())
			except KeyboardInterrupt:
				print("NEXT COMMAND.")

		print('[1] ' + cmd_2)

		if not args.debug:
			path = 'records'
			dirs = sorted(os.listdir(path))
			print(dirs)
			cmd_2 += f' --wav_file_name records/{dirs[-1]}/audio.wav'
			subprocess.run(cmd_2.split())

		sys.exit()

	elif args.action == 'transcribe':
		cmd_2 += f' --model {args.model}'
		cmd_2 += f' --wav_file_name {args.wav_file_name}'
		print('[0] ' + cmd_2)
		if not args.debug:
			subprocess.run(cmd_2.split())
		sys.exit()

	elif args.action == 'read':
		cmd += f' --action {args.action}'
		cmd += f' --wav_file_name {args.wav_file_name}'
		print('[0] ' + cmd)
		if not args.debug:
			subprocess.run(cmd.split())
		sys.exit()
	elif args.action == 'play':
		cmd += f' --action {args.action}'
		cmd += f' --wav_file_name {args.wav_file_name}'
		print('[0] ' + cmd)
		if not args.debug:
			subprocess.run(cmd.split())
		sys.exit()



