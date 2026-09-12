#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transcribe ONE time window of the video, with gain applied, to check whether the
narration is recoverable at all.  Usage: python3 slice_probe.py <start_sec> <dur_sec>
Prints the transcript so it can be compared against the site's claims."""
import os
import subprocess
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MP4 = os.path.join(SITE, "录像45 Sales order processing.mp4")
OUTDIR = os.path.join(HERE, "audio", "probe")
os.makedirs(OUTDIR, exist_ok=True)

start = float(sys.argv[1])
dur = float(sys.argv[2]) if len(sys.argv) > 2 else 105.0
gain = sys.argv[3] if len(sys.argv) > 3 else "24dB"
wav = os.path.join(OUTDIR, "s%04d_%s.wav" % (int(start), gain))

# extract + mono 16k + gain (the recording is very quiet: ~-42 dBFS)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", "%.2f" % start,
                "-t", "%.2f" % dur, "-i", MP4, "-vn", "-ac", "1", "-ar", "16000",
                "-af", "volume=%s,alimiter=limit=0.95" % gain, wav, "-y"], check=True)

import mlx_whisper  # noqa: E402
r = mlx_whisper.transcribe(wav, path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                           language="en", verbose=False, condition_on_previous_text=False,
                           temperature=0.0, no_speech_threshold=0.6)
txt = " ".join(s["text"].strip() for s in r["segments"])
print("=== window %.0f-%.0f s, gain %s, %d segments ===" % (start, start + dur, gain, len(r["segments"])))
print(" ".join(txt.split())[:2600])
