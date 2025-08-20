from PIL import Image
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
img = Image.open(src).convert('RGBA')
# sizes for ico
sizes = [(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)]
img.save(dst, format='ICO', sizes=sizes)
print(f"Wrote {dst}")
