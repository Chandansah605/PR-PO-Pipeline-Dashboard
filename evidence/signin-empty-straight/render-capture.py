from pathlib import Path
import sys

from PIL import Image


frame_dir = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
frames = sorted(frame_dir.glob("*.jpg"))
if len(frames) < 2:
    raise SystemExit("At least two screencast frames are required")

images = [Image.open(frame).convert("RGB") for frame in frames]
timestamps = [float(frame.stem.split("-", 1)[1]) for frame in frames]
durations = [
    max(16, round((timestamps[index + 1] - timestamp) * 1000))
    for index, timestamp in enumerate(timestamps[:-1])
]
durations.append(round(sum(durations[-10:]) / min(10, len(durations))))
try:
    images[0].save(
        output,
        format="WEBP",
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0,
        quality=76,
        method=4,
    )
finally:
    for image in images:
        image.close()
