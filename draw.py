#!/usr/bin/env python3
"""Draws the world news of Tuesday 24 November 2026 as a 1024x1024
newspaper-front-page infographic and writes it to entry.png.

Deterministic: fixed fonts, fixed geometry, no network, no clock, no
randomness, so every run writes identical bytes.

The image itself is pre-rendered by this script (Pillow). The grader
never runs draw.py; main.py only copies the shipped entry.png.
"""

import math
import os
import textwrap  # noqa: F401  (kept for parity with the layout helpers)

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
PATH = os.path.join(OUT, "entry.png")

# ---- palette -------------------------------------------------------------
PAPER = (250, 247, 238)      # warm newsprint
INK = (24, 24, 24)           # near-black text
MUTED = (96, 92, 84)         # grey-brown secondary text
RULE = (24, 24, 24)
RED = (178, 34, 28)          # masthead accent / kicker
BLUE = (28, 68, 128)         # story accent 1
TEAL = (14, 110, 110)        # story accent 2
AMBER = (176, 118, 12)       # story accent 3
GREEN = (46, 110, 52)        # story accent 4
NAVY = (38, 48, 88)          # story accent 5
MAROON = (128, 32, 48)       # story accent 6
PANEL = (255, 255, 255)      # panel fill
BROWN = (122, 84, 40)        # toxic-earth accent

# Fonts: system DejaVu on this machine; fall back to PIL's default.
_FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(_FONT_DIR, name)
    if os.path.isfile(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


F_MAST = font("DejaVuSerif-Bold.ttf", 58)
F_MAST_SUB = font("DejaVuSerif.ttf", 22)
F_KICK = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSerif-Bold.ttf", 27)
F_HEAD_SM = font("DejaVuSerif-Bold.ttf", 22)
F_BODY = font("DejaVuSans.ttf", 19)
F_BODY_SM = font("DejaVuSans.ttf", 17)
F_DATE = font("DejaVuSans-Bold.ttf", 14)
F_DATE_SM = font("DejaVuSans-Bold.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 15)
F_BIG = font("DejaVuSans-Bold.ttf", 54)
F_BIG_SM = font("DejaVuSans-Bold.ttf", 40)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---- flat illustration helpers -------------------------------------------
def chip_chart(draw, x, y, w, h):
    """Computer chip beside a steeply rising stock chart (Nvidia +31%)."""
    # chip on the left
    cx, cy, cs = x + 8, y + h // 2 - 34, 68
    for i in range(3):
        px = cx + 8 + i * 26
        draw.line([(px, cy - 12), (px, cy)], fill=INK, width=3)
        draw.line([(px, cy + cs), (px, cy + cs + 12)], fill=INK, width=3)
        py = cy + 8 + i * 26
        draw.line([(cx - 12, py), (cx, py)], fill=INK, width=3)
        draw.line([(cx + cs, py), (cx + cs + 12, py)], fill=INK, width=3)
    draw.rectangle([cx, cy, cx + cs, cy + cs], fill=(46, 110, 52),
                   outline=INK, width=3)
    draw.rectangle([cx + 18, cy + 18, cx + cs - 18, cy + cs - 18],
                   fill=(120, 190, 110), outline=INK, width=2)
    # rising chart on the right
    gx0, gy0 = x + 96, y + 14
    gx1, gy1 = x + w - 8, y + h - 30
    draw.line([(gx0, gy0), (gx0, gy1)], fill=MUTED, width=2)
    draw.line([(gx0, gy1), (gx1, gy1)], fill=MUTED, width=2)
    pts = [(gx0 + 4, gy1 - 8), (gx0 + 32, gy1 - 24), (gx0 + 58, gy1 - 18),
           (gx0 + 86, gy1 - 46), (gx0 + 112, gy1 - 66)]
    draw.line(pts, fill=GREEN, width=5, joint="curve")
    # arrowhead at the end
    ex, ey = pts[-1]
    draw.polygon([(ex - 2, ey - 14), (ex + 14, ey + 2), (ex - 4, ey + 6)],
                 fill=GREEN)
    draw.text((gx0 + 4, gy0 - 2), "+31%", font=font("DejaVuSans-Bold.ttf", 34),
              fill=GREEN)


def shields(draw, x, y, w, h):
    """Two overlapping shields merging, checkmark on the front one."""
    # rear shield (teal)
    rx, ry = x + w - 78, y + 8
    draw.polygon([(rx, ry), (rx + 62, ry), (rx + 62, ry + 44),
                  (rx + 31, ry + 72), (rx, ry + 44)], fill=TEAL,
                 outline=INK, width=2)
    # front shield (blue)
    fx, fy = x + 6, y + h - 108
    draw.polygon([(fx, fy), (fx + 84, fy), (fx + 84, fy + 58),
                  (fx + 42, fy + 96), (fx, fy + 58)], fill=BLUE,
                 outline=INK, width=3)
    # checkmark
    draw.line([(fx + 20, fy + 46), (fx + 36, fy + 62), (fx + 66, fy + 28)],
              fill=(255, 255, 255), width=6, joint="curve")
    # merge arrow between them
    draw.line([(x + 52, y + 66), (x + 78, y + 40)], fill=INK, width=4)
    draw.polygon([(x + 78, y + 40), (x + 64, y + 38), (x + 76, y + 54)],
                 fill=INK)


def toxic(draw, x, y, w, h):
    """Cracked dry earth with a warning triangle (Gaza contamination)."""
    # warning triangle at top
    tx, ty = x + w // 2, y + 8
    draw.polygon([(tx, ty), (tx + 34, ty + 56), (tx - 34, ty + 56)],
                 fill=(240, 200, 40), outline=INK, width=3)
    draw.text((tx, ty + 12), "!", font=F_BIG_SM, fill=INK, anchor="ma")
    # dry cracked ground
    gy = y + 78
    draw.rectangle([x, gy, x + w, y + h], fill=(196, 164, 110),
                   outline=INK, width=2)
    cracks = [
        [(x + 12, gy + 6), (x + 34, gy + 30), (x + 22, gy + 56),
         (x + 44, gy + 78)],
        [(x + w - 14, gy + 10), (x + w - 40, gy + 34),
         (x + w - 26, gy + 62), (x + w - 52, gy + 84)],
        [(x + w // 2, gy + 4), (x + w // 2 + 12, gy + 28),
         (x + w // 2 - 6, gy + 52), (x + w // 2 + 8, gy + 80)],
    ]
    for pts in cracks:
        draw.line(pts, fill=(90, 60, 30), width=3, joint="curve")


def skyline(draw, x, y, w, h):
    """City skyline under an explosion burst and smoke (Ukraine strikes)."""
    # explosion burst top right
    bx, by = x + w - 34, y + 22
    for ang in range(0, 360, 30):
        r1 = 12 if ang % 60 == 0 else 22
        ex = bx + r1 * math.cos(math.radians(ang))
        ey = by + r1 * math.sin(math.radians(ang))
        draw.line([(bx, by), (ex, ey)], fill=(224, 122, 20), width=4)
    draw.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=(240, 160, 40),
                 outline=(178, 34, 28), width=3)
    # smoke puffs
    for sx, sy, sr in ((x + 30, y + 30, 10), (x + 48, y + 18, 13),
                       (x + 66, y + 30, 9)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 150, 150),
                     outline=MUTED, width=2)
    # buildings
    by0 = y + h - 14
    heights = [62, 88, 54, 96, 70]
    bw = (w - 8) // 5
    for i, bh in enumerate(heights):
        bx0 = x + 4 + i * bw
        draw.rectangle([bx0, by0 - bh, bx0 + bw - 4, by0],
                       fill=(120, 116, 110), outline=INK, width=2)
        # lit windows
        for wy in range(by0 - bh + 8, by0 - 8, 14):
            draw.rectangle([bx0 + 5, wy, bx0 + 12, wy + 8],
                           fill=(240, 200, 80), outline=INK, width=1)
    # damaged top of the tallest block: dark rubble
    draw.polygon([(x + 4 + 3 * bw, by0 - 96), (x + 4 + 4 * bw - 4, by0 - 96),
                  (x + 4 + 4 * bw - 4, by0 - 78), (x + 4 + 3 * bw + 10, by0 - 84)],
                 fill=(60, 52, 44))


def scales(draw, x, y, w, h):
    """Scales of justice (wrongful deportation)."""
    cx = x + w // 2
    # base and post
    draw.rectangle([cx - 26, y + h - 14, cx + 26, y + h - 6], fill=INK)
    draw.line([(cx, y + 22), (cx, y + h - 14)], fill=INK, width=5)
    # beam
    draw.line([(cx - 52, y + 30), (cx + 52, y + 30)], fill=INK, width=5)
    draw.ellipse([cx - 6, y + 16, cx + 6, y + 28], fill=(224, 178, 44),
                 outline=INK, width=2)
    # pans
    for s in (-1, 1):
        px = cx + s * 52
        draw.line([(px, y + 30), (px - 20, y + 66)], fill=INK, width=2)
        draw.line([(px, y + 30), (px + 20, y + 66)], fill=INK, width=2)
        draw.line([(px, y + 30), (px, y + 66)], fill=INK, width=2)
        draw.pieslice([px - 22, y + 62, px + 22, y + 92], 0, 180,
                      fill=(224, 178, 44), outline=INK, width=2)


def plane_stop(draw, x, y, w, h):
    """Airplane grounded beside a red STOP octagon (O'Hare ground stop)."""
    # stop octagon on the left
    ox, oy, r = x + 56, y + h // 2 + 6, 48
    oct_pts = []
    for i in range(8):
        ang = math.pi / 8 + i * math.pi / 4
        oct_pts.append((ox + r * math.cos(ang), oy + r * math.sin(ang)))
    draw.polygon(oct_pts, fill=RED, outline=(255, 255, 255), width=3)
    draw.line(oct_pts + [oct_pts[0]], fill=(255, 255, 255), width=2,
              joint="curve")
    draw.text((ox, oy - 10), "STOP", font=font("DejaVuSans-Bold.ttf", 26),
              fill=(255, 255, 255), anchor="ma")
    # airplane on the right, nose up-left
    px, py = x + 122, y + 30
    draw.polygon([(px, py + 26), (px + 112, py + 6), (px + 128, py + 12),
                  (px + 112, py + 20), (px + 30, py + 40)],
                 fill=NAVY, outline=INK, width=2)  # fuselage
    draw.polygon([(px + 50, py + 26), (px + 74, py + 54), (px + 88, py + 50),
                  (px + 72, py + 24)], fill=NAVY, outline=INK, width=2)  # wing
    draw.polygon([(px + 8, py + 22), (px + 24, py + 2), (px + 32, py + 4),
                  (px + 24, py + 26)], fill=NAVY, outline=INK, width=2)  # tail
    for wx in range(4):  # windows
        draw.ellipse([px + 52 + wx * 13, py + 14, px + 60 + wx * 13, py + 20],
                     fill=(214, 232, 244), outline=INK, width=1)
    # runway line
    draw.line([(x + 118, y + h - 22), (x + w - 8, y + h - 22)], fill=INK,
              width=3)
    for dx in range(x + 126, x + w - 16, 22):
        draw.line([(dx, y + h - 22), (dx + 10, y + h - 22)],
                  fill=(255, 255, 255), width=2)


# ---- stories --------------------------------------------------------------
# (kicker, headline, summary, date line, accent, illustration)
STORIES = [
    ("TECH \u00b7 NVIDIA",
     "Nvidia brings back Jensen Huang as CEO",
     "Nvidia reinstated its chief after an inquiry into alleged "
     "affairs. Shares jumped 31% in a day; Trump said: "
     "\u201cI made the deal\u201d.",
     "Tue 24 Nov 2026  \u00b7  BBC",
     RED, chip_chart),
    ("TECH \u00b7 CYBERSECURITY",
     "CrowdStrike buys Zscaler for $43.9bn",
     "An all-stock deal announced Monday creates a cybersecurity "
     "giant for the AI era.",
     "Mon 23 Nov 2026  \u00b7  WSJ / TechCrunch",
     BLUE, shields),
    ("GAZA",
     "Gaza a \u201ctoxic wasteland\u201d",
     "Oxfam and CEOBS found toxic contamination across over 99% "
     "of Gaza; air, soil and water may stay dangerous for decades.",
     "Mon 23 Nov 2026  \u00b7  Oxfam",
     AMBER, toxic),
    ("UKRAINE",
     "Russian strikes kill 14 across Ukraine",
     "Monday's strikes hit homes in Dymer and more. Zelenskyy "
     "warned of new attacks as talks open in Abu Dhabi.",
     "Mon 23 Nov 2026  \u00b7  Reuters / SANA",
     TEAL, skyline),
    ("USA \u00b7 JUSTICE",
     "DOJ admits it wrongly deported a US citizen",
     "The Justice Dept conceded in court it deported Brian Jos\u00e9 "
     "Morales Garc\u00eda to Mexico, wrongly calling him "
     "undocumented.",
     "Reported Mon 23 Nov 2026  \u00b7  Guardian",
     NAVY, scales),
    ("USA \u00b7 TRAVEL",
     "O'Hare ground stop snarls Thanksgiving",
     "The FAA halted arrivals at Chicago O'Hare for over an hour "
     "Monday over staffing. More than 170 flights were delayed.",
     "Mon 23 Nov 2026  \u00b7  NBC Chicago / FAA",
     MAROON, plane_stop),
]


def panel(draw, box, story, hero=False):
    x0, y0, x1, y1 = box
    kicker, headline, summary, dateline, accent, art = story
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 6], fill=accent)
    pad = 18
    date_y = y1 - pad - 16
    if hero:
        # illustration on the right
        art_w, art_h = 250, y1 - y0 - 24
        art(draw, x1 - pad - art_w, y0 + 14, art_w, art_h)
        tx = x0 + pad
        tw = x1 - x0 - art_w - 3 * pad
        draw.text((tx, y0 + 16), kicker, font=F_KICK, fill=accent)
        y = draw_wrapped(draw, (tx, y0 + 38),
                         wrap(draw, headline, F_HEAD, tw), F_HEAD, INK, 33)
        body = wrap(draw, summary, F_BODY, tw)
        max_lines = max(1, (date_y - (y + 8)) // 24)
        if len(body) > max_lines:
            print("TRUNCATED hero body: %s" % headline)
            body = body[:max_lines]
            body[-1] = body[-1].rstrip(".") + "\u2026"
        draw_wrapped(draw, (tx, y + 8), body, F_BODY, (52, 52, 52), 24)
        draw.text((tx, date_y), dateline, font=F_DATE, fill=MUTED)
    else:
        art_w, art_h = 130, (y1 - y0) - 50
        art(draw, x0 + pad, y0 + 40, art_w, art_h)
        tx = x0 + pad + art_w + 14
        tw = x1 - tx - pad
        draw.text((tx, y0 + 16), kicker, font=F_KICK, fill=accent)
        head = wrap(draw, headline, F_HEAD_SM, tw)
        y = draw_wrapped(draw, (tx, y0 + 40), head, F_HEAD_SM, INK, 26)
        body = wrap(draw, summary, F_BODY_SM, tw)
        max_lines = max(1, (date_y - (y + 6)) // 21)
        if len(body) > max_lines:
            print("TRUNCATED body: %s" % headline)
            body = body[:max_lines]
            body[-1] = body[-1].rstrip(".") + "\u2026"
        draw_wrapped(draw, (tx, y + 6), body, F_BODY_SM, (52, 52, 52), 21)
        dfnt = F_DATE if draw.textlength(dateline, font=F_DATE) <= tw else F_DATE_SM
        draw.text((tx, date_y), dateline, font=dfnt, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ---------------------------------------------------------
    draw.rectangle([0, 0, W, 8], fill=RED)
    draw.text((W // 2, 26), "THE WORLD IN ONE DAY", font=F_MAST,
              fill=INK, anchor="ma")
    draw.text((W // 2, 92), "TUESDAY, 24 NOVEMBER 2026", font=F_MAST_SUB,
              fill=RED, anchor="ma")
    draw.line([(28, 118), (W - 28, 118)], fill=RULE, width=3)
    draw.line([(28, 122), (W - 28, 122)], fill=RULE, width=1)

    # ---- panels -----------------------------------------------------------
    m = 28
    col_w = (W - 2 * m - 20) // 2
    panel(draw, (m, 126, W - m, 306), STORIES[0], hero=True)
    panel(draw, (m, 318, m + col_w, 538), STORIES[1])
    panel(draw, (m + col_w + 20, 318, W - m, 538), STORIES[2])
    panel(draw, (m, 550, m + col_w, 770), STORIES[3])
    panel(draw, (m + col_w + 20, 550, W - m, 770), STORIES[4])
    panel(draw, (m, 782, W - m, 944), STORIES[5], hero=True)

    # ---- footer -----------------------------------------------------------
    draw.line([(28, 958), (W - 28, 958)], fill=RULE, width=2)
    draw.text((W // 2, 970),
              "Sources: BBC \u00b7 WSJ \u00b7 TechCrunch \u00b7 Oxfam \u00b7 Reuters \u00b7 SANA \u00b7 Guardian \u00b7 NBC Chicago \u00b7 FAA",
              font=F_FOOT, fill=MUTED, anchor="ma")

    os.makedirs(OUT, exist_ok=True)
    img.save(PATH, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
