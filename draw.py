#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: a one-page newspaper front page.

1024x1024 PNG, warm newsprint, six panels, one per story of the
20 November 2026 news cycle. Everything is drawn from scratch with
Pillow; no photos, no downloaded assets. Deterministic output:
running this script twice produces byte-identical PNGs.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# ---- palette: restrained newsprint -------------------------------------
PAPER = (245, 238, 221)      # warm newsprint
PANEL = (253, 249, 238)      # lighter panel fill
INK = (31, 26, 20)           # near-black text
MUTED = (107, 95, 74)        # warm grey for source lines
RULE = (163, 51, 39)         # deep editorial red
RED = (163, 51, 39)
BLUE = (44, 74, 107)
TEAL = (42, 110, 120)
GOLD = (185, 138, 30)
GREEN = (74, 110, 66)
BORDER = (138, 125, 99)

serif_b = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", s)
serif = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", s)
sans_b = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", s)
sans = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", s)

F_TITLE = serif_b(56)
F_DATE = sans_b(23)
F_TAG = sans(13)
F_KICK = sans_b(13)
F_HEAD = serif_b(21)
F_BODY = sans(15)
F_SRC = sans_b(12)


def wrap(draw, text, font, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, cx, y, text, font, fill=INK):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


# ---- small flat illustrations, one per story (100x100 box) -------------
def art_summit(d, x, y):
    # Three flags over a round table: Shenzhen skyline behind.
    sky = (58, 84, 110)
    for i, h in enumerate((34, 52, 44, 60, 38)):
        bx = x + 4 + i * 19
        d.rectangle([bx, y + 78 - h, bx + 14, y + 78], fill=sky)
    # table
    d.ellipse([x + 18, y + 78, x + 82, y + 94], fill=(120, 84, 50))
    d.rectangle([x + 46, y + 92, x + 54, y + 100], fill=(120, 84, 50))
    # flags on poles: US (stripes + canton), China (red + stars),
    # Russia (white / blue / red bands)
    for i in range(3):
        fx = x + 12 + i * 30
        d.line([fx + 7, y + 6, fx + 7, y + 78], fill=INK, width=2)
    # US flag
    fx = x + 12
    for j, c in enumerate([(178, 34, 52), (245, 245, 245), (178, 34, 52),
                           (245, 245, 245)]):
        d.rectangle([fx + 7, y + 8 + j * 4, fx + 27, y + 8 + j * 4 + 4], fill=c)
    d.rectangle([fx + 7, y + 8, fx + 15, y + 16], fill=(44, 74, 160))
    # China flag
    fx = x + 42
    d.rectangle([fx + 7, y + 8, fx + 27, y + 24], fill=(222, 41, 16))
    d.ellipse([fx + 10, y + 11, fx + 14, y + 15], fill=(255, 220, 60))
    for sx, sy in [(19, 10), (22, 13), (19, 16), (16, 14)]:
        d.ellipse([fx + sx, y + sy, fx + sx + 2, y + sy + 2], fill=(255, 220, 60))
    # Russia flag
    fx = x + 72
    for j, c in enumerate([(245, 245, 245), (44, 74, 160), (200, 40, 40)]):
        d.rectangle([fx + 7, y + 8 + j * 5, fx + 27, y + 8 + j * 5 + 5], fill=c)


def art_court(d, x, y):
    # Courthouse: pediment, columns, base; scales of justice above.
    d.polygon([(x + 8, y + 34), (x + 50, y + 12), (x + 92, y + 34)], fill=BLUE)
    d.rectangle([x + 10, y + 34, x + 90, y + 38], fill=INK)
    for i in range(4):
        cx = x + 18 + i * 22
        d.rectangle([cx, y + 40, cx + 10, y + 84], fill=(220, 210, 185))
        d.rectangle([cx - 2, y + 38, cx + 12, y + 42], fill=INK)
        d.rectangle([cx - 2, y + 82, cx + 12, y + 86], fill=INK)
    d.rectangle([x + 8, y + 86, x + 92, y + 94], fill=INK)
    # scales
    d.line([x + 50, y + 2, x + 50, y + 12], fill=GOLD, width=2)
    d.line([x + 36, y + 4, x + 64, y + 4], fill=GOLD, width=2)
    d.arc([x + 30, y + 4, x + 42, y + 14], 0, 180, fill=GOLD, width=2)
    d.arc([x + 58, y + 4, x + 70, y + 14], 0, 180, fill=GOLD, width=2)


def art_iran(d, x, y):
    # Calendar page marked JAN 2027, with a pause sign.
    d.rectangle([x + 14, y + 10, x + 86, y + 92], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([x + 14, y + 10, x + 86, y + 34], fill=RED)
    d.text((x + 50 - d.textlength("JAN 2027", font=sans_b(13)) / 2, y + 15),
           "JAN 2027", font=sans_b(13), fill=(255, 255, 255))
    for r in range(3):
        for c in range(5):
            gx, gy = x + 22 + c * 12, y + 42 + r * 14
            d.rectangle([gx, gy, gx + 8, gy + 8], outline=MUTED, width=1)
    # pause bars over the calendar
    d.rectangle([x + 40, y + 52, x + 47, y + 78], fill=BLUE)
    d.rectangle([x + 53, y + 52, x + 60, y + 78], fill=BLUE)


def art_cyclone(d, x, y):
    # Spiral storm over a coastline.
    cx, cy = x + 50, y + 40
    for i, r in enumerate((8, 16, 24, 32)):
        start = 200 + i * 70
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 260,
              fill=TEAL, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=TEAL)
    # coastline + house, bottom left
    d.line([x + 6, y + 88, x + 94, y + 88], fill=INK, width=2)
    d.polygon([(x + 10, y + 78), (x + 20, y + 68), (x + 30, y + 78)], fill=RED)
    d.rectangle([x + 13, y + 78, x + 27, y + 88], fill=(220, 210, 185))
    # rain, bottom right
    for i in range(4):
        rx = x + 66 + i * 8
        d.line([rx, y + 70, rx - 3, y + 80], fill=BLUE, width=2)


def art_gta(d, x, y):
    # City skyline at dusk, gold sun, big dollar badge.
    d.ellipse([x + 58, y + 8, x + 92, y + 42], fill=GOLD)
    for i, h in enumerate((46, 64, 38, 72, 52, 60)):
        bx = x + 4 + i * 16
        d.rectangle([bx, y + 96 - h, bx + 13, y + 96], fill=(40, 40, 56))
        d.rectangle([bx + 4, y + 96 - h + 6, bx + 9, y + 96 - h + 11],
                    fill=(255, 220, 120))
    d.ellipse([x + 6, y + 52, x + 40, y + 86], fill=(245, 245, 245),
              outline=GOLD, width=3)
    d.text((x + 23 - d.textlength("$", font=sans_b(24)) / 2, y + 56),
           "$", font=sans_b(24), fill=GOLD)


def art_europe(d, x, y):
    # Two speech bubbles: EU blue with gold stars, partner gold.
    d.rounded_rectangle([x + 8, y + 12, x + 66, y + 52], radius=10, fill=BLUE)
    d.polygon([(x + 18, y + 50), (x + 26, y + 66), (x + 30, y + 50)], fill=BLUE)
    for i, (sx, sy) in enumerate([(24, 24), (37, 20), (50, 24), (30, 34), (44, 34)]):
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=GOLD)
    d.rounded_rectangle([x + 34, y + 56, x + 92, y + 88], radius=10, fill=GOLD)
    d.polygon([(x + 72, y + 86), (x + 64, y + 98), (x + 62, y + 86)], fill=GOLD)
    d.text((x + 63 - d.textlength("OK", font=sans_b(13)) / 2, y + 66),
           "OK", font=sans_b(13), fill=(255, 255, 255))


ART = {
    "summit": art_summit,
    "court": art_court,
    "iran": art_iran,
    "cyclone": art_cyclone,
    "gta": art_gta,
    "europe": art_europe,
}

STORIES = [
    dict(kicker="DIPLOMACY", art="summit",
         head="Three leaders, one table",
         body=("Trump, Xi and Putin meet as a trio for the first time, in "
               "Shenzhen on the APEC sidelines. Nuclear arms control, "
               "energy security and the world's wars top the agenda. "
               "Eighty-one minutes, a joint statement — and no deals."),
         src="CNN · LE MONDE"),
    dict(kicker="JUSTICE", art="court",
         head="Genocide verdict: a world first",
         body=("The UN's top court rules Myanmar committed genocide "
               "against the Rohingya in 2017 — the first such verdict "
               "against a state in its 80-year history. The court also "
               "ordered reparations and a report within two years."),
         src="UN NEWS · CNN"),
    dict(kicker="WASHINGTON", art="iran",
         head="No rush on Iran: wait until 2027",
         body=("\"We'll see what happens after January 1,\" Trump says of "
               "Iran, as reports swirl of Tehran weighing chemical and "
               "biological weapons. Israel is pressing for strikes; "
               "Trump says there is no imminent threat to Washington."),
         src="REUTERS"),
    dict(kicker="WEATHER", art="cyclone",
         head="Cyclone Akvan hits Odisha",
         body=("Landfall due at noon on India's east coast. More than "
               "80,000 people evacuated, 74 rescue teams deployed, "
               "winds of 90–100 km/h. Schools are shut across 11 "
               "districts as heavy rain lashes the coast."),
         src="THE HINDU · IMD"),
    dict(kicker="CULTURE", art="gta",
         head="GTA 6 banks $1.84bn in a day",
         body=("Rockstar's launch passes The Odyssey's entire $1.8bn "
               "global box-office run in 24 hours — an estimate; "
               "Take-Two has confirmed no figure yet. Some 19 million "
               "copies sold, PlayStation leading three-to-one."),
         src="REUTERS · SENSOR TOWER"),
    dict(kicker="EUROPE", art="europe",
         head="Europe ready to talk to Russia",
         body=("At a Berlin summit, European leaders say they will "
               "negotiate with Moscow to end the Ukraine war — but "
               "only on terms acceptable to Kyiv. Putin has so far "
               "rejected any European role in the US-led talks."),
         src="BBC"),
]


def draw_panel(d, x, y, w, h, story):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER, width=1)
    pad = 14
    # kicker
    d.text((x + pad, y + 12), story["kicker"], font=F_KICK, fill=RED)
    # illustration, top right
    ax, ay = x + w - pad - 100, y + 10
    d.rectangle([ax - 4, ay - 4, ax + 104, ay + 104], outline=BORDER, width=1)
    ART[story["art"]](d, ax, ay)
    # headline, left of the illustration
    hw = w - pad * 2 - 108
    lines = wrap(d, story["head"], F_HEAD, hw)
    hy = y + 34
    for line in lines[:3]:
        d.text((x + pad, hy), line, font=F_HEAD, fill=INK)
        hy += 26
    # hairline under the header zone
    d.line([x + pad, y + 118, x + w - pad, y + 118], fill=BORDER, width=1)
    # body, full width
    bw = w - pad * 2
    blines = wrap(d, story["body"], F_BODY, bw)
    by = y + 130
    for line in blines[:5]:
        d.text((x + pad, by), line, font=F_BODY, fill=INK)
        by += 21
    # source line, bottom right
    d.text((x + w - pad - d.textlength(story["src"], font=F_SRC), y + h - 24),
           story["src"], font=F_SRC, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer double border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    d.rectangle([16, 16, W - 17, H - 17], outline=BORDER, width=1)

    # ---- masthead ----
    text_center(d, W // 2, 34, "The World in One Day", F_TITLE)
    d.line([60, 108, W - 60, 108], fill=RULE, width=3)
    d.line([60, 113, W - 60, 113], fill=RULE, width=1)
    text_center(d, W // 2, 124, "FRIDAY, 20 NOVEMBER 2026", F_DATE)
    text_center(d, W // 2, 152,
                "Six stories that defined the day — in one page.",
                F_TAG, fill=MUTED)

    # ---- grid: 2 columns x 3 rows ----
    gx, gy = 26, 178
    gw = (W - 2 * gx - 16) // 2          # 478
    gh = (H - gy - 26 - 2 * 12) // 3     # 267
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_panel(d, gx + col * (gw + 16), gy + row * (gh + 12),
                   gw, gh, story)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
