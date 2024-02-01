#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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"
)

# apply pretrained pipeline
diarization = pipeline("../results/20240131-test/raw.wav")

# print the result
res = []
print(res)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    start = turn.start
    end   = turn.end
    res.append({
        "start": start,
        "end": end,
        "speaker": speaker
    })
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

with open("../results/20240131-test/diarization.yaml", "w") as f:
    yaml.dump(res, f, default_flow_style=False, indent=4, allow_unicode=True, sort_keys=False)