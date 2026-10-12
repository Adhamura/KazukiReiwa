# Makes Documentation/Demo.gif: the nine weights, then each supported script typed out.
#   python3 Documentation/make-demo.py        (needs Pillow; run from the repository root)
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF = os.path.join(ROOT, "Fonts", "TrueType", "KazukiReiwa-{}.ttf")
OUT = os.path.join(ROOT, "Documentation", "Demo.gif")
W, H = 800, 420
PAPER, INK, DIM, ACCENT = (250, 248, 244), (22, 22, 28), (150, 150, 160), (232, 86, 86)
WEIGHTS = ["Thin", "ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black"]
SCRIPTS = [
    ("Latin", "The quick brown fox jumps over the lazy dog"),
    ("Cyrillic", "Съешь же ещё этих мягких французских булок"),
    ("Greek", "Ξεσκεπάζω την ψυχοφθόρα βδελυγμία"),
    ("Japanese", "いろはにほへと ちりぬるを 令和"),
    ("Braille", "⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙"),
]


def font(weight, size):
    return ImageFont.truetype(TTF.format(weight), size)


def canvas():
    im = Image.new("RGB", (W, H), PAPER)
    return im, ImageDraw.Draw(im)


def footer(d, text):
    d.text((40, H - 46), text, font=font("Medium", 20), fill=DIM)


frames, durations = [], []


def add(im, ms):
    frames.append(im)
    durations.append(ms)


# 1. the name through all nine weights, the "Aaあ" sample following
for w in WEIGHTS + WEIGHTS[-2:0:-1]:
    im, d = canvas()
    d.text((40, 30), "KazukiReiwa", font=font(w, 92), fill=INK)
    d.text((40, 150), "Aa", font=font(w, 150), fill=INK)
    d.text((270, 150), "あ", font=font(w, 150), fill=ACCENT)
    d.text((450, 175), "Жж Ωω", font=font(w, 92), fill=INK)
    footer(d, w)
    add(im, 520 if w in ("Thin", "Black") else 260)

# 2. each script typed out, then held
for name, text in SCRIPTS:
    f = font("Regular", 44 if name != "Braille" else 64)
    lines, cur = [], ""
    for word in text.split(" "):  # wrap to the frame
        t = (cur + " " + word).strip()
        if ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(t, font=f) <= W - 80:
            cur = t
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    full = "\n".join(lines)
    steps = list(range(2, len(full) + 1, 2 if len(full) > 30 else 1)) + [len(full)]
    for n in steps:
        im, d = canvas()
        d.text((40, 40), name.upper(), font=font("SemiBold", 24), fill=ACCENT)
        d.multiline_text((40, 96), full[:n], font=f, fill=INK, spacing=18)
        footer(d, "KazukiReiwa · SIL Open Font License")
        add(im, 45)
    durations[-1] = 1300

# 3. closing card
im, d = canvas()
d.text((40, 110), "KazukiReiwa", font=font("Black", 96), fill=INK)
d.text((44, 240), "Latin · Cyrillic · Greek · Japanese · Braille", font=font("Regular", 30), fill=INK)
d.text((44, 290), "9 weights + variable · TTF and OTF · free (OFL)", font=font("Regular", 26), fill=DIM)
add(im, 2600)

pal = [f.quantize(colors=64, method=Image.Quantize.MEDIANCUT) for f in frames]
pal[0].save(OUT, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
print(OUT, os.path.getsize(OUT) // 1024, "KB,", sum(durations) / 1000, "s")
