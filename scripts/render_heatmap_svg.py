import json
from pathlib import Path

with open("data/contributions.json", "r") as f:
    data = json.load(f)

CELL = 12
GAP = 3

LEFT = 40
TOP = 40

weeks = []

week = []

for day in data:

    week.append(day)

    if len(week) == 7:
        weeks.append(week)
        week = []

if week:
    weeks.append(week)

PALETTE = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}

svg = []

WIDTH = len(weeks) * (CELL + GAP) + 80
HEIGHT = 7 * (CELL + GAP) + 100

svg.append(f'''
<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">
''')

svg.append("""
<style>

.square{
opacity:0;
transform:translateY(8px);
animation:appear .35s forwards;
}

@keyframes appear{

to{

opacity:1;
transform:translateY(0);

}

}

</style>

<rect
width="100%"
height="100%"
fill="#0d1117"/>
""")

for week_index, week in enumerate(weeks):

    for day_index, day in enumerate(week):

        x = LEFT + week_index * (CELL + GAP)
        y = TOP + day_index * (CELL + GAP)

        level = min(day["level"], 4)

        color = PALETTE.get(level, PALETTE[0])

        delay = (week_index * 7 + day_index) * 0.008

        svg.append(f"""
<rect
class="square"
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="2"
fill="{color}">

<animate
attributeName="opacity"
from="0"
to="1"
dur=".25s"
begin="{delay}s"
fill="freeze"/>

<animateTransform
attributeName="transform"
type="translate"
from="0 8"
to="0 0"
dur=".25s"
begin="{delay}s"
fill="freeze"/>

<title>
{day["date"]}
</title>

</rect>
""")
        # -----------------------------
# Title
# -----------------------------

svg.append(f"""
<text
x="40"
y="20"
font-family="Consolas, monospace"
font-size="16"
fill="#c9d1d9">

GitHub Contributions

</text>
""")

# -----------------------------
# Legend
# -----------------------------

legend_x = WIDTH - 120
legend_y = HEIGHT - 30

svg.append(f"""
<text
x="{legend_x-35}"
y="{legend_y+10}"
font-family="Consolas"
font-size="11"
fill="#8b949e">

Less

</text>
""")

legend_colors = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353"
]

for i, color in enumerate(legend_colors):

    svg.append(f"""
<rect
x="{legend_x+i*16}"
y="{legend_y}"
width="10"
height="10"
rx="2"
fill="{color}"/>
""")

svg.append(f"""
<text
x="{legend_x+90}"
y="{legend_y+10}"
font-family="Consolas"
font-size="11"
fill="#8b949e">

More

</text>
""")

# -----------------------------
# Total Contributions
# -----------------------------

total = sum(day["count"] for day in data)

svg.append(f"""
<text
x="40"
y="{HEIGHT-20}"
font-family="Consolas"
font-size="12"
fill="#58a6ff">

{total} contributions in the last year

</text>
""")

svg.append("</svg>")

Path("contrib-heatmap.svg").write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print("contrib-heatmap.svg created!")