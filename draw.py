#!/usr/bin/env python3
"""Render the 24 November 2026 one-day news front page as entry.png.

A newspaper front page: serif masthead with the date, then a 2x3 grid of
story panels. Each panel carries a coloured kicker, a headline, a short
summary, a source line, and a small flat vector illustration drawn with
plain PIL shapes. Everything is measured before it is drawn so no text
can overflow its panel.
"""

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT_PATH = "entry.png"

PAGE = 1024
MARGIN = 30
INK = (26, 26, 26)
PAPER = (246, 241, 231)
PANEL_FILL = (255, 255, 255)
MUTED = (96, 92, 84)
RED = (178, 34, 34)

# (kicker, accent colour, headline, summary, dateline)
STORIES = [
    (
        "TECH · NVIDIA",
        (118, 185, 0),
        "Nvidia brings back Jensen Huang as CEO",
        "Nvidia reinstated its chief after an inquiry into alleged "
        "extramarital affairs. Shares jumped 31% in a day; Trump said: "
        "\u201cI made the deal\u201d.",
        "Tue 24 Nov 2026 \u00b7 BBC",
    ),
    (
        "TECH · CYBERSECURITY",
        (21, 101, 192),
        "CrowdStrike buys Zscaler for $43.9bn",
        "An all-stock deal announced Monday creates a cybersecurity "
        "giant for the AI era.",
        "Mon 23 Nov 2026 \u00b7 WSJ / TechCrunch",
    ),
    (
        "GAZA",
        (183, 121, 31),
        "Gaza a \u2018toxic wasteland\u2019",
        "Oxfam and CEOBS found toxic contamination across over 99% of "
        "Gaza; air, soil and water may stay dangerous for decades.",
        "Mon 23 Nov 2026 \u00b7 Oxfam",
    ),
    (
        "UKRAINE",
        (0, 87, 183),
        "Russian strikes kill 14 across Ukraine",
        "Monday\u2019s strikes hit homes in Dymer and more. Zelenskyy "
        "warned of new attacks as talks open in Abu Dhabi.",
        "Mon 23 Nov 2026 \u00b7 Reuters / SANA",
    ),
    (
        "USA · JUSTICE",
        (38, 50, 56),
        "DOJ admits it wrongly deported a US citizen",
        "The Justice Dept conceded in court it deported Brian Jos\u00e9 "
        "Morales Garc\u00eda to Mexico, wrongly calling him undocumented.",
        "Reported Mon 23 Nov 2026 \u00b7 Guardian",
    ),
    (
        "USA · TRAVEL",
        (0, 105, 92),
        "O\u2019Hare ground stop snarls Thanksgiving",
        "The FAA halted arrivals at Chicago O\u2019Hare for over an hour "
        "Monday over staffing. More than 170 flights were delayed.",
        "Mon 23 Nov 2026 \u00b7 NBC Chicago / FAA",
    ),
]


def load_font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_BOLD = load_font("DejaVuSerif-Bold.ttf", 58)
SANS_BOLD = load_font("DejaVuSans-Bold.ttf", 26)
SANS = load_font("DejaVuSans.ttf", 17)
SANS_SMALL = load_font("DejaVuSans.ttf", 14)
KICKER_FONT = load_font("DejaVuSans-Bold.ttf", 14)
DATE_FONT = load_font("DejaVuSans-Bold.ttf", 27)
SUB_FONT = load_font("DejaVuSans.ttf", 16)


def wrap_text(canvas, text, font, max_width):
    """Split text into lines that each fit max_width, word by word."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            trial = f"{current} {word}".strip()
            if canvas.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def fit_or_fail(canvas, text, font, max_width, max_lines, label):
    lines = wrap_text(canvas, text, font, max_width)
    if len(lines) > max_lines:
        raise ValueError(f"{label}: needs {len(lines)} lines, only {max_lines} fit")
    return lines


def draw_masthead(canvas):
    """Title, date line and rules across the top of the page."""
    canvas.line([(MARGIN, 34), (PAGE - MARGIN, 34)], fill=INK, width=4)
    title = "THE WORLD IN ONE DAY"
    tw = canvas.textlength(title, font=SERIF_BOLD)
    canvas.text(((PAGE - tw) / 2, 44), title, font=SERIF_BOLD, fill=INK)
    date_line = "TUESDAY, 24 NOVEMBER 2026"
    dw = canvas.textlength(date_line, font=DATE_FONT)
    canvas.text(((PAGE - dw) / 2, 118), date_line, font=DATE_FONT, fill=RED)
    sub = "Six stories that defined the day"
    sw = canvas.textlength(sub, font=SUB_FONT)
    canvas.text(((PAGE - sw) / 2, 152), sub, font=SUB_FONT, fill=MUTED)
    canvas.line([(MARGIN, 182), (PAGE - MARGIN, 182)], fill=INK, width=2)
    canvas.line([(MARGIN, 187), (PAGE - MARGIN, 187)], fill=INK, width=1)


def draw_chip(canvas, box):
    """Story 1: a green computer chip with pins and a rising arrow."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle(box, radius=10, fill=(27, 94, 32))
    for i in range(3):
        px = x0 + 14 + i * 18
        canvas.rectangle([px, y0 - 6, px + 8, y0 + 2], fill=(27, 94, 32))
        canvas.rectangle([px, y1 - 2, px + 8, y1 + 6], fill=(27, 94, 32))
    canvas.rectangle([x0 + 16, y0 + 16, x1 - 16, y1 - 16], fill=(118, 185, 0))
    canvas.rectangle([x0 + 30, y0 + 30, x1 - 30, y1 - 30], fill=(27, 94, 32))
    canvas.line(
        [(x0 + 24, y1 - 26), (x0 + 40, y1 - 40), (x0 + 50, y1 - 32), (x0 + 66, y1 - 48)],
        fill=(255, 255, 255),
        width=4,
    )
    canvas.polygon(
        [(x0 + 66, y1 - 48), (x0 + 56, y1 - 48), (x0 + 66, y1 - 38)],
        fill=(255, 255, 255),
    )


def draw_shields(canvas, box):
    """Story 2: two overlapping shields merging into one."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle(box, radius=10, fill=(232, 240, 254))
    canvas.polygon(
        [(x0 + 12, y0 + 12), (x0 + 44, y0 + 12), (x0 + 44, y0 + 44),
         (x0 + 28, y0 + 60), (x0 + 12, y0 + 44)],
        fill=(21, 101, 192),
    )
    canvas.polygon(
        [(x0 + 40, y0 + 20), (x0 + 72, y0 + 20), (x0 + 72, y0 + 52),
         (x0 + 56, y0 + 68), (x0 + 40, y0 + 52)],
        fill=(198, 40, 40),
    )
    canvas.line([(x0 + 34, y0 + 46), (x0 + 50, y0 + 46)], fill=(255, 255, 255), width=5)
    canvas.line([(x0 + 42, y0 + 38), (x0 + 42, y0 + 54)], fill=(255, 255, 255), width=5)


def draw_hazard(canvas, box):
    """Story 3: a warning triangle over cracked ground."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle(box, radius=10, fill=(255, 243, 224))
    cx = (x0 + x1) // 2
    canvas.polygon(
        [(cx, y0 + 10), (x1 - 12, y1 - 22), (x0 + 12, y1 - 22)],
        fill=(255, 193, 7),
        outline=(26, 26, 26),
        width=3,
    )
    canvas.rectangle([cx - 3, y0 + 30, cx + 3, y0 + 48], fill=(26, 26, 26))
    canvas.ellipse([cx - 3, y0 + 54, cx + 3, y0 + 60], fill=(26, 26, 26))
    canvas.line([(x0 + 12, y1 - 12), (x0 + 30, y1 - 6), (x0 + 48, y1 - 12),
                 (x0 + 66, y1 - 6), (x1 - 12, y1 - 12)],
                fill=(121, 85, 72), width=3)


def draw_flag(canvas, box):
    """Story 4: blue-over-yellow bands with a building and smoke."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle(box, radius=10, fill=(0, 87, 183))
    canvas.rectangle([x0, (y0 + y1) // 2, x1, y1 - 10], fill=(255, 215, 0))
    canvas.rounded_rectangle(box, radius=10, outline=(26, 26, 26), width=2)
    canvas.rectangle([x0 + 16, y0 + 34, x0 + 34, y1 - 14], fill=(38, 50, 56))
    canvas.rectangle([x0 + 40, y0 + 44, x0 + 54, y1 - 14], fill=(38, 50, 56))
    canvas.rectangle([x0 + 60, y0 + 28, x0 + 74, y1 - 14], fill=(38, 50, 56))
    for sx, sy, r in ((x0 + 26, y0 + 18, 5), (x0 + 36, y0 + 12, 4), (x0 + 48, y0 + 16, 5)):
        canvas.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))


def draw_court(canvas, box):
    """Story 5: a courthouse front with columns and pediment."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle(box, radius=10, fill=(236, 239, 241))
    canvas.polygon(
        [(x0 + 8, y0 + 34), ((x0 + x1) // 2, y0 + 12), (x1 - 8, y0 + 34)],
        fill=(38, 50, 56),
    )
    canvas.ellipse([((x0 + x1) // 2) - 5, y0 + 22, ((x0 + x1) // 2) + 5, y0 + 32],
                   fill=(255, 255, 255))
    for i in range(3):
        cx = x0 + 18 + i * 24
        canvas.rectangle([cx, y0 + 38, cx + 8, y1 - 16], fill=(38, 50, 56))
    canvas.rectangle([x0 + 10, y1 - 16, x1 - 10, y1 - 10], fill=(38, 50, 56))


def draw_plane(canvas, box):
    """Story 6: a sleek plane in profile under a red stop octagon."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle(box, radius=10, fill=(224, 242, 241))
    # Fuselage: a long body tapering to a pointed nose on the right.
    canvas.polygon(
        [(x0 + 10, y0 + 52), (x0 + 16, y0 + 44), (x0 + 56, y0 + 44),
         (x0 + 72, y0 + 51), (x0 + 56, y0 + 58), (x0 + 16, y0 + 58)],
        fill=(0, 105, 92),
    )
    # Tail fin rising at the back, wing sweeping down from the middle.
    canvas.polygon([(x0 + 16, y0 + 46), (x0 + 26, y0 + 32), (x0 + 30, y0 + 46)],
                   fill=(0, 105, 92))
    canvas.polygon([(x0 + 36, y0 + 58), (x0 + 46, y0 + 70), (x0 + 50, y0 + 58)],
                   fill=(0, 105, 92))
    # Two cabin windows.
    canvas.ellipse([x0 + 52, y0 + 48, x0 + 57, y0 + 53], fill=(255, 255, 255))
    canvas.ellipse([x0 + 60, y0 + 48, x0 + 65, y0 + 53], fill=(255, 255, 255))
    oct_cx, oct_cy, oct_r = x1 - 22, y0 + 20, 15
    pts = []
    for k in range(8):
        import math
        ang = math.pi / 8 + k * math.pi / 4
        pts.append((oct_cx + oct_r * math.cos(ang), oct_cy + oct_r * math.sin(ang)))
    canvas.polygon(pts, fill=(198, 40, 40))
    canvas.line([(oct_cx - 6, oct_cy - 6), (oct_cx + 6, oct_cy + 6)],
                fill=(255, 255, 255), width=3)
    canvas.line([(oct_cx - 6, oct_cy + 6), (oct_cx + 6, oct_cy - 6)],
                fill=(255, 255, 255), width=3)


ILLUSTRATORS = [draw_chip, draw_shields, draw_hazard, draw_flag, draw_court, draw_plane]


def draw_panel(canvas, rect, story, illustrator):
    """One story panel: kicker, illustration, headline, summary, source."""
    kicker, accent, headline, summary, dateline = story
    x0, y0, x1, y1 = rect
    pad = 16
    canvas.rounded_rectangle(rect, radius=6, fill=PANEL_FILL, outline=(200, 195, 185), width=2)
    canvas.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 8], fill=accent)

    # Kicker pill, top left.
    kw = canvas.textlength(kicker, font=KICKER_FONT) + 18
    canvas.rounded_rectangle([x0 + pad, y0 + 18, x0 + pad + kw, y0 + 42],
                             radius=11, fill=accent)
    canvas.text((x0 + pad + 9, y0 + 21), kicker, font=KICKER_FONT, fill=(255, 255, 255))

    # Flat illustration, top right.
    icon = (x1 - pad - 84, y0 + 16, x1 - pad, y0 + 100)
    illustrator(canvas, icon)

    # Headline: two lines max, width stops short of the illustration.
    head_w = (x1 - pad - 96) - (x0 + pad)
    head_lines = fit_or_fail(canvas, headline, SANS_BOLD, head_w, 3, headline)
    hy = y0 + 52
    for line in head_lines:
        canvas.text((x0 + pad, hy), line, font=SANS_BOLD, fill=INK)
        hy += 31

    # Summary: full panel width, three lines max.
    sum_w = (x1 - pad) - (x0 + pad)
    sum_lines = fit_or_fail(canvas, summary, SANS, sum_w, 3, headline)
    sy = y0 + 118
    for line in sum_lines:
        canvas.text((x0 + pad, sy), line, font=SANS, fill=(48, 46, 42))
        sy += 23

    # Source line pinned to the bottom.
    canvas.line([(x0 + pad, y1 - 34), (x1 - pad, y1 - 34)], fill=(220, 215, 205), width=1)
    canvas.text((x0 + pad, y1 - 28), dateline, font=SANS_SMALL, fill=MUTED)


def main():
    image = Image.new("RGB", (PAGE, PAGE), PAPER)
    canvas = ImageDraw.Draw(image)
    draw_masthead(canvas)

    grid_top = 202
    grid_bottom = PAGE - MARGIN
    gap = 14
    col_w = (PAGE - 2 * MARGIN - gap) // 2
    row_h = (grid_bottom - grid_top - 2 * gap) // 3
    for idx, story in enumerate(STORIES):
        row, col = divmod(idx, 2)
        px0 = MARGIN + col * (col_w + gap)
        py0 = grid_top + row * (row_h + gap)
        draw_panel(canvas, (px0, py0, px0 + col_w, py0 + row_h),
                   story, ILLUSTRATORS[idx])

    image.save(OUT_PATH, "PNG")
    print(f"wrote {OUT_PATH} ({image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
