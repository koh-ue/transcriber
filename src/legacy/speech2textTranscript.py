#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: FIXME: XXX: HACK: NOTE: INTENT: USAGE:

import os
import re
import sys
import json
import wave
#import joblib
import argparse
#import functools
#import itertools
#import numpy as np
import pandas as pd
#import seaborn as sns
from google.cloud import speech
from google.cloud import storage
from google.api_core.exceptions import NotFound
#from collections import defaultdict

#import numexpr as ne
#ne.set_num_threads(16)

sys.path.append(".")

from src.library.misc.jsons import print_json

parser = argparse.ArgumentParser(add_help=True)

parser.add_argument("-i", "--input_file", type=str, required=True)
parser.add_argument("-b", "--bucket_name", type=str, default="audio-recorder")
parser.add_argument("-l", "--language", type=str, default='en-US', help="Available languages are liseted in https://cloud.google.com/speech-to-text/docs/languages?hl=ja")
#parser.add_argument("--condition", type=str, choices=["sunny", "rainy", "cloudy"], default="sunny")
#parser.add_argument("--is_competition", action="store_true")

args = parser.parse_args()


# NOTE: AREA for functions.

def get_wav_info(input_file):
    with wave.open(input_file, 'rb') as wr:
        num_channel = wr.getnchannels()
        sample_width = wr.getsampwidth()
        sample_rate = wr.getframerate()
        frame_rate = wr.getnframes()
    
    wav_info = {"Number of Channels": num_channel, "Sample Width":sample_width, "Sample Rate": sample_rate, "Frame Rate":frame_rate, "Length": 1.0*frame_rate/sample_rate}
    print_json(json.dumps(wav_info, indent=4))

    return wav_info
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def transcribe_long_file_from_gcs(gcs_uri, sample_rate, lang, num_channels): # USAGE: Available languages are liseted in LANGUAGES. Please use .html for searching.
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=lang,
        audio_channel_count=num_channels,
        enable_separate_recognition_per_channel=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=9000)

    df_transcript = pd.DataFrame(columns=["First alternative of result", "Transcript", "Channel Tag"])
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        print("Transcript: {}".format(alternative.transcript))
        print("Channel Tag: {}".format(result.channel_tag))

        df_transcript = df_transcript.append({"First alternative of result": i, "Transcript": alternative.transcript, "Channel Tag": result.channel_tag}, ignore_index=True)
    
    return df_transcript




if __name__ == '__main__':
    destination_info = {
        "Input File": args.input_file,
        "Language": args.language,
        "Output Name": f"s2t-{os.path.splitext(os.path.basename(args.input_file))[0]}_{args.language}",
        "Bucket Name": args.bucket_name,
        "Blob Name": os.path.basename(args.input_file),
        "Gcs Url": f'gs://{args.bucket_name}/{os.path.basename(args.input_file)}',
        "Save Directory": os.path.dirname(args.input_file),
    }
    print_json(json.dumps(destination_info, indent=4))

    wav_info = get_wav_info(args.input_file)
    save_pkl = f"{destination_info['Save Directory']}/{destination_info['Output Name']}.pkl"
    is_pkl = os.path.isfile(save_pkl)

    if is_pkl:
        print("pkl Already exsits ...")
        df_transcript = pd.read_pickle(save_pkl)
    else:
        try:
            df_transcript = transcribe_long_file_from_gcs(gcs_uri=destination_info["Gcs Url"], 
                                                          sample_rate=wav_info["Sample Rate"], 
                                                          lang=args.language, 
                                                          num_channels=wav_info["Number of Channels"])
        except NotFound:
            upload_blob(bucket_name=destination_info["Bucket Name"],
                        source_file_name=destination_info["Input File"],
                        destination_blob_name=destination_info["Blob Name"])
            
            df_transcript = transcribe_long_file_from_gcs(gcs_uri=destination_info["Gcs Url"],
                                                          sample_rate=wav_info["Sample Rate"],
                                                          lang=args.language,num_channels=wav_info["Number of Channels"])
    
        df_transcript.to_pickle(save_pkl)
    

    # INTENT: Following codes are for generating script text. You can change following codes flexibly.

    df_formatted = df_transcript #[df_transcript["Channel Tag"] == 0]
    transcript_list = df_formatted["Transcript"].to_list()

    txt_file = destination_info["Save Directory"] + f'/{destination_info["Output Name"]}.txt'
    with open(txt_file, "w") as f:
        f.write('\n\n'.join(transcript_list))

