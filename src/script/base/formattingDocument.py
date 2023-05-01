#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: FIXME: XXX: HACK: NOTE: INTENT: USAGE:

import os
import re
import sys
import json
import pprint
import argparse
import numpy as np
import pandas as pd

sys.path.append(".")

parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-i', "--input_file", type=str, required=True)

args = parser.parse_args()


# NOTE: AREA for functions.

def txt_to_list(input_file):
    lines_list = []
    with open(input_file, 'r') as f:
        for each_line in f:
            if each_line != '\n':
                lines_list.append(each_line.replace('\n', ''))
    return lines_list

def separate_lines_on_speakers(lines_list):
    sentences = []
    each_sentence = []
    for line in lines_list:
        if ":" in line:
            sentences.append(each_sentence)
            each_sentence = [line]
        else:
            each_sentence.append(line)
    sentences.pop(0)
    return sentences

def make_sentences_into_text(sentences):
    # INTENT: Add '\n' as last with .join()
    text_lines_list = []
    for each_sentence in sentences:
        if len(each_sentence) == 1:
            text_lines_list.append(each_sentence[0])
        else:
            sentence = ', '.join(each_sentence) + "."
            text_lines_list.append(sentence)
    
    text = '\n'.join(text_lines_list)
    return text


if __name__ == '__main__':
    lines = txt_to_list(args.input_file)
    sentences = separate_lines_on_speakers(lines)
    text = make_sentences_into_text(sentences)

    save_file = os.path.dirname(args.input_file) + "/minutes.txt"
    with open(save_file, 'w') as f:
        f.write(text)
    
    
