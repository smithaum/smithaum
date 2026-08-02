from pathlib import Path

WIDTH = 520
HEIGHT = 340

rows = [
    ("Name", "Smitha U M"),
    ("Role", "Frontend Developer"),
    ("College", "Jyothy Institute of Technology"),
    ("Language", "Python • JavaScript • Java"),
    ("Framework", "React • Node.js"),
    ("Cloud", "AWS"),
    ("Tools", "Git • Docker • VS Code"),
    ("GitHub", "@smithaum"),
]

svg = []

svg.append(f"""
<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}">

<style>

text {{
font-family: Consolas, monospace;
}}

.value {{
fill:#58a6ff;
}}

.key {{
fill:#7ee787;
}}

.row {{
opacity:0;
animation: fade .4s forwards;
}}

@keyframes fade {{
to {{ opacity:1; }}
}}

</style>

<rect
x="0"
y="0"
width="{WIDTH}"
height="{HEIGHT}"
rx="12"
fill="#0d1117"/>

<rect
x="0"
y="0"
width="{WIDTH}"
height="36"
rx="12"
fill="#161b22"/>

<circle cx="22" cy="18" r="6" fill="#ff5f56"/>
<circle cx="42" cy="18" r="6" fill="#ffbd2e"/>
<circle cx="62" cy="18" r="6" fill="#27c93f"/>

<text
x="260"
y="23"
fill="#c9d1d9"
font-size="14"
text-anchor="middle">

whoami

</text>
""")

y = 65

for i, (key, value) in enumerate(rows):

    delay = i * 0.15

    svg.append(f"""
<g class="row">

<animate
attributeName="opacity"
from="0"
to="1"
dur=".3s"
begin="{delay}s"
fill="freeze"/>

<text
class="key"
x="25"
y="{y}"
font-size="15">

{key}

</text>

<text
class="value"
x="150"
y="{y}"
font-size="15">

{value}

</text>

</g>
""")

    y += 32

svg.append("</svg>")

Path("info-card.svg").write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print("info-card.svg created!")