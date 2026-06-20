import subprocess
import re

def clear_terminal():
    print("\033[H\033[J", end="")

def analyze_audio(path):
    """Detect leading/trailing silence (seconds) and total duration (seconds)
    from an audio file using ffmpeg's silencedetect filter."""
    log = subprocess.run(
        f'ffmpeg -i "{path}" -af silencedetect=noise=-30dB:d=0.3 -f null -',
        shell=True,
        text=True,
        capture_output=True,
    ).stderr

    duration = 0.0
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", log)
    if match:
        hours, minutes, seconds = match.groups()
        duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

    starts = [float(s) for s in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(s) for s in re.findall(r"silence_end: ([\d.]+)", log)]

    # Leading silence: a silence region that begins at (or near) the very start.
    leading = ends[0] if starts and ends and starts[0] < 0.5 else 0.0

    # Trailing silence: a silence region that begins but never ends (runs to EOF).
    trailing = duration - starts[-1] if len(starts) > len(ends) and duration else 0.0

    return leading, trailing, duration
