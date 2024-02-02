#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import argparse
import collections
import numpy as np

def who_speak(t, diar):
    for item in diar:
        if item["start"] < t and t < item["end"]:
            return item["speaker"]
    return "none"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--target', type=str, required=True)
    parser.add_argument('--max-delta', type=int, default=4)
    args = parser.parse_args()

    with open(f"{args.target}/diarization.yaml", "r") as f:
        diarization = yaml.safe_load(f)
    with open(f"{args.target}/result.yaml", "r") as f:
        conversation = yaml.safe_load(f)

    timings = np.arange(int(conversation["segments"][-1]["end"]))

    max_delta = args.max_delta
    _labels = []
    for _t in timings:
        for delta in range(max_delta):
            t = _t + delta/max_delta
            _labels.append([float(t), who_speak(t, diar=diarization)])
    labels = np.array(_labels)

    for segment in conversation["segments"]:
        _label_of_segment = []
        for t in np.arange(int(segment["start"]*max_delta)/max_delta, int(segment["end"]*max_delta)/max_delta, 0.25):
            idx = np.where(labels==str(t))[0].astype(np.int64)
            if len(labels[idx, -1]):
                _label_of_segment.append(labels[idx, -1])
        _labels_seg = np.array(_label_of_segment).flatten()
        labels_seg = _labels_seg[_labels_seg != "none"]
        counted = collections.Counter(labels_seg)
        segment_label = counted.most_common()[0][0]
        segment["label"] = str(segment_label)
    
    with open(f"{args.target}/diarized-result.yaml", "w") as f:
        yaml.dump(conversation, f, default_flow_style=False, indent=4, allow_unicode=True, sort_keys=False)