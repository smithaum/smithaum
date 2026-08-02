from pathlib import Path
from PIL import Image

ASCII_CHARS = " .`:-=+*cs#%@"

# -----------------------------
# Image Processing
# -----------------------------

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))


def grayify(image):
    return image.convert("L")


def pixels_to_ascii(image):
    pixels = image.getdata()

    ascii_str = ""

    for pixel in pixels:
        index = pixel * (len(ASCII_CHARS)-1) // 255
        ascii_str += ASCII_CHARS[index]

    return ascii_str


# -----------------------------
# Main
# -----------------------------

image = Image.open("source-prepped.png")

image = resize_image(image)
image = grayify(image)

ascii_data = pixels_to_ascii(image)

width = image.width

ascii_lines = [
    ascii_data[i:i+width]
    for i in range(0, len(ascii_data), width)
]

# Save text version
Path("ascii.txt").write_text("\n".join(ascii_lines), encoding="utf-8")

# -----------------------------
# SVG Generation
# -----------------------------

# -----------------------------
# Animated SVG Generation
# -----------------------------

FONT_SIZE = 8
LINE_HEIGHT = 10
CHAR_WIDTH = 5
WINDOW_PADDING = 20
TITLE_BAR = 35

svg_width = width * CHAR_WIDTH + 20
svg_height = len(ascii_lines) * LINE_HEIGHT + 20

svg = []

svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">

<style>
@keyframes blink {{
    50% {{ opacity:0; }}
}}
.cursor {{
    animation: blink .8s infinite;
}}
</style>

<rect width="100%" height="100%" fill="#0d1117"/>
''')

for i, line in enumerate(ascii_lines):

    delay = i * 0.08

    y = 15 + i * LINE_HEIGHT

    clip_id = f"clip{i}"

    svg.append(f"""
<clipPath id="{clip_id}">
    <rect x="10"
          y="{y-8}"
          width="0"
          height="{LINE_HEIGHT}">
        <animate
            attributeName="width"
            from="0"
            to="{svg_width}"
            dur="0.6s"
            begin="{delay}s"
            fill="freeze"/>
    </rect>
</clipPath>
""")

    svg.append(f"""
<text
x="10"
y="{y}"
font-family="Consolas, monospace"
font-size="{FONT_SIZE}"
fill="#d0d0d0"
clip-path="url(#{clip_id})"
xml:space="preserve">
{line}
</text>
""")

last_y = 15 + (len(ascii_lines)-1)*LINE_HEIGHT

svg.append(f"""
<text
class="cursor"
x="{svg_width-25}"
y="{last_y}"
font-family="Consolas"
font-size="{FONT_SIZE}"
fill="#39d353">
█
</text>
""")

svg.append("</svg>")

Path("avi-ascii.svg").write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print("Animated SVG created!")