#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import argparse
from pyannote.audio import Pipeline

sys.path.append("./utils")
sys.path.append("./src/library")

from loggers import Log
from core.whisperanscript import Whisperancript



if __name__ == '__main__':
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('--file-name', type=str, required=True)
	parser.add_argument('--destination', type=str, required=True)
	parser.add_argument('--model', default='base')
	parser.add_argument('--language', type=str, default='en')
	args = parser.parse_args()

	logger = Log(name=__name__, file=__file__, no_file=False).logger
	logger.info(f"running {__file__}")

	model = Whisperancript(
		filename    = args.file_name,
		destination = args.destination,
		model       = args.model,
		logger      = logger
	)
	model.transcribe(lang=args.language)
	
	logger.info("Now diarizing ...")
	pipeline = Pipeline.from_pretrained(
		"pyannote/speaker-diarization-3.1",
		use_auth_token="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"
	)
	diarization = pipeline(model.wav_filename)
	res = []
	for turn, _, speaker in diarization.itertracks(yield_label=True):
		start = turn.start
		end   = turn.end
		res.append({
			"start": start,
			"end": end,
			"speaker": speaker
		})
		logger.info(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

	with open(f"{args.destination}/diarization.yaml", "w") as f:
		yaml.dump(res, f, default_flow_style=False, indent=4, allow_unicode=True, sort_keys=False)
	logger.info("Finish diarizing ...")