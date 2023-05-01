#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import wave
import pyaudio
import argparse
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

BOLD_RED = "\033[1;31m"
BOLD_GREEN = "\033[1;32m"
BOLD_YELLOW = "\033[1;33m"
BOLD_BLUE = "\033[1;34m"
END = "\033[0m"

parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-a', '--action', type=str, choices=['get_mic', 'record', 'read', 'play'], default='record',\
                    help='get_mic->shows a microphone list. record->records an audio. read->shows waves and FFT of an audio file. play->plays an audio file.')
parser.add_argument('-c', '--channel', type=int, default=0, help='CHANNEL must be from channel index from --debug.')
parser.add_argument('-r', '--recording_time', type=str, default='0-0-5', help='RECOEDING_TIME should be [HOURS]-[MINUTES]-[SECONDS].')
parser.add_argument('-w', '--wav_file_name', type=str, default='', help='WAV_FILE_NAME is for read and play.')

args = parser.parse_args()

def GetMicIndex():
    ''' マイクチャンネルのindexをリストで取得する '''
 
    # 最大入力チャンネル数が0でない項目をマイクチャンネルとしてリストに追加
    pa = pyaudio.PyAudio()
    mic_list = []
    for i in range(pa.get_device_count()):
        num_of_input_ch = pa.get_device_info_by_index(i)['maxInputChannels']
 
        if num_of_input_ch != 0:
            mic_list.append([pa.get_device_info_by_index(i)['name'], pa.get_device_info_by_index(i)['index']])
 
    return pd.DataFrame(mic_list, columns=['DEVICE_NAME', 'CHANNEL'])

def FormatTime(time_in_hours_minutes_seconds):
    try:
        raw_time = time_in_hours_minutes_seconds
        np_time = np.array(raw_time.split('-'), dtype=int)
        print(BOLD_GREEN + f"Recording time: {np_time[0]}h {np_time[1]}min {np_time[2]}sec" + END)
    except:
        print(BOLD_RED + "ERROR in FormatTime!" + END)
        sys.exit()
    return np_time
 
def MakeWavFile(Record_Seconds, channel, save = True):
    """
    Redord audio and save.
    """
    chunk = 1024
    FORMAT = pyaudio.paInt16
    
    CHANNELS = 1 # Fixed as 1 for Monaural
    RATE = 44100 #Fixed as 44100 (Sample rate)
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = channel)
    
    print("Now Recording...")
    all_data = []
    bar = tqdm(total = Record_Seconds)
    bar.set_description('Progress')

    try:
        for i in range(0, int(RATE / chunk * Record_Seconds)):
            if (i+1)%int(RATE / chunk) == 0:
                bar.update(1)
            data = stream.read(chunk)
            all_data.append(data)
        bar.close()
    except KeyboardInterrupt:
        bar.close()

    print("Finished Recording.")
    
    stream.close()
    p.terminate()

    dt_now = datetime.datetime.now()
    dir_name = dt_now.strftime('records/%Y-%m-%d-%H-%M-%S/')
    os.makedirs(dir_name, exist_ok=True)
    
    FileName = dir_name + 'audio.wav'
    if save:
        wavFile = wave.open(FileName, 'wb')
        wavFile.setnchannels(CHANNELS)
        wavFile.setsampwidth(p.get_sample_size(FORMAT))
        wavFile.setframerate(RATE)
        wavFile.writeframes(b"".join(all_data))
        wavFile.close()
    

    
def ReadWavFile(FileName):
    """
    Read wav file and show waves and FFT.
    """
    try:
        wr = wave.open(FileName, "r")
    except FileNotFoundError:
        print("[Error 404] No such file or directory: " + FileName)
        return 0
    data = wr.readframes(wr.getnframes())
    wr.close()
    x = np.frombuffer(data, dtype="int16") / float(2**15)

    plt.figure(figsize=(15,3))
    plt.plot(x)
    plt.show()
    
    x = np.fft.fft(np.frombuffer(data, dtype="int16"))
    plt.figure(figsize=(15,3))
    plt.plot(x.real[:int(len(x)/2)])
    plt.show()
    
    
    
def PlayWavFie(Filename):
    """
    Play wav file.
    """
    try:
        wf = wave.open(Filename, "r")
    except FileNotFoundError: #ファイルが存在しなかった場合
        print("[Error 404] No such file or directory: " + Filename)
        return 0
        
    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # チャンク単位でストリームに出力し音声を再生
    print("Now Playing...")
    chunk = 1024
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()
    print("Finish Playing...")

    

if __name__ == "__main__":
    if args.action == 'get_mic':
        mic_list = GetMicIndex()
        print(mic_list)

    elif args.action == 'record':
        np_time = FormatTime(args.recording_time)
        time_in_second = np.sum(np_time * np.array([3600, 60, 1]))
        MakeWavFile(Record_Seconds = time_in_second, channel = args.channel)

    elif args.action == 'read':
        ReadWavFile(args.wav_file_name)

    elif args.action == 'play':
        PlayWavFie(args.wav_file_name)
    










