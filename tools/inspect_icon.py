from PIL import Image
from pathlib import Path
import sys

p = Path(sys.argv[1])
if not p.exists():
    print(f"Icon not found: {p}")
    sys.exit(2)

img = Image.open(p)
print(f"Format: {img.format}")
try:
    sizes = img.info.get('sizes')
    print(f"Sizes (info.sizes): {sizes}")
except Exception:
    pass

# Try iterating frames (ICO stores images as frames)
frames = []
try:
    for i in range(10):
        img.seek(i)
        frames.append(img.size)
except EOFError:
    pass

print(f"Frames (sizes): {frames}")
print(f"Mode: {img.mode}")
print('OK')
