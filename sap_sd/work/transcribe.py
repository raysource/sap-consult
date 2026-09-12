#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transcribe the training video's narration with mlx-whisper (segments + timestamps)."""
import json
import sys
import mlx_whisper

WAV = "/Users/jason/Desktop/work/training/sap_sd/work/audio/audio.wav"
OUT = "/Users/jason/Desktop/work/training/sap_sd/work/audio/transcript.json"
MODEL = "mlx-community/whisper-large-v3-turbo"

r = mlx_whisper.transcribe(
    WAV,
    path_or_hf_repo=MODEL,
    language="en",
    verbose=False,
    word_timestamps=False,
    condition_on_previous_text=False,
)
segs = [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()}
        for s in r["segments"]]
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump({"language": r.get("language"), "segments": segs}, fh, ensure_ascii=False, indent=1)
print("segments:", len(segs))
print("first:", segs[0] if segs else None)
print("last:", segs[-1] if segs else None)
