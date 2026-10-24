"""Mix VO: suprapune liniile Supertonic la timpii beat-urilor -> film/audio/mix.wav (43.6s)."""
import os
import subprocess

BASE = os.path.expanduser("~/AI/romanian-s2s/film")
VO = os.path.join(BASE, "audio", "vo")
TOTAL = 43.6

TIMES = [
    ("line01", 0.0),
    ("line02", 3.45),
    ("line03", 9.70),
    ("line04", 17.0),
    ("line05", 23.4),
    ("line06", 29.5),
    ("line07", 37.0),
]

cmd = ["ffmpeg", "-y"]
filter_parts = []
labels = []
for i, (name, t) in enumerate(TIMES):
    cmd += ["-i", os.path.join(VO, name + ".wav")]
    ms = int(t * 1000)
    filter_parts.append("[{}:a]adelay={}:all=1[a{}]".format(i, ms, i))
    labels.append("[a{}]".format(i))

filter_parts.append("".join(labels) + "amix=inputs={}:normalize=0,apad=pad_dur=2[out]".format(len(TIMES)))
cmd += ["-filter_complex", ";".join(filter_parts), "-map", "[out]", "-t", str(TOTAL),
        os.path.join(BASE, "audio", "mix.wav")]
subprocess.run(cmd, check=True)
print("mix.wav scris ({}s)".format(TOTAL))
