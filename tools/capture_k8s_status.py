import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "screenshots" / "kubernetes-status.png"


def run(*args):
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.rstrip()


sections = [
    ("$ kubectl get deployment hello-world", run("kubectl", "get", "deployment", "hello-world")),
    ("$ kubectl get pods -l app=hello-world -o wide", run("kubectl", "get", "pods", "-l", "app=hello-world", "-o", "wide")),
    ("$ kubectl get service hello-world", run("kubectl", "get", "service", "hello-world")),
]

text = "\n\n".join(f"{title}\n{body}" for title, body in sections)
font_path = Path(r"C:\Windows\Fonts\consola.ttf")
font = ImageFont.truetype(str(font_path), 19)
title_font = ImageFont.truetype(str(font_path), 20)

padding = 32
line_height = 27
lines = text.splitlines()
max_width = max(ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(line, font=font) for line in lines)
width = max(1200, int(max_width + padding * 2))
height = padding * 2 + line_height * len(lines) + 48

image = Image.new("RGB", (width, height), "#111827")
draw = ImageDraw.Draw(image)
draw.rounded_rectangle((14, 14, width - 14, height - 14), radius=12, fill="#0b1020", outline="#334155", width=2)

y = padding
for line in lines:
    color = "#86efac" if line.startswith("$") else "#e5e7eb"
    draw.text((padding, y), line, font=title_font if line.startswith("$") else font, fill=color)
    y += line_height

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
image.save(OUTPUT)
print(OUTPUT)
