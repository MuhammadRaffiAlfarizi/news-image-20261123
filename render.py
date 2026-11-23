#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page, 1024x1024 PNG.

Build-time tool for the make.fun news-image-20261123 entry. The entry itself
(main.py) only copies the rendered entry.png; this script is kept in the repo
so anyone can see how the image was made. Deterministic: no randomness, no
dates from the clock, no network.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (180, 35, 24)
NAVY = (29, 53, 87)
OCHRE = (176, 124, 22)
TEAL = (31, 94, 90)
GREY = (90, 86, 78)
LIGHT = (233, 226, 210)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, max_w, fill=INK, leading=None, align="left"):
    x, y = xy
    lh = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        if align == "center":
            lx = x + (max_w - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x, y, w, color=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


def kicker(draw, x, y, text, color=RED, size=21):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=color)
    return f


# ------------------------------------------------------------------ icons
def icon_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 110, 165),
                 outline=NAVY, width=4)
    # land blobs
    draw.ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.05, cy - r * 0.05],
                 fill=(74, 140, 74))
    draw.ellipse([cx + r * 0.05, cy + r * 0.05, cx + r * 0.62, cy + r * 0.55],
                 fill=(74, 140, 74))
    draw.ellipse([cx - r * 0.15, cy - r * 0.75, cx + r * 0.3, cy - r * 0.35],
                 fill=(74, 140, 74))
    # crack
    draw.line([(cx - r * 0.3, cy - r * 0.7), (cx - r * 0.05, cy - r * 0.25),
               (cx - r * 0.3, cy + r * 0.1), (cx, cy + r * 0.55)],
              fill=RED, width=5)
    # smoke puffs above
    for i, (sx, sy, sr) in enumerate([(cx - 52, cy - r - 18, 16),
                                     (cx - 18, cy - r - 34, 20),
                                     (cx + 22, cy - r - 20, 15)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 146, 138))


def icon_tanker(draw, x, y, w, h):
    # sea
    for i in range(3):
        yy = y + h - 22 + i * 9
        draw.arc([x, yy - 8, x + w, yy + 8], 0, 180, fill=NAVY, width=3)
    # hull
    draw.polygon([(x + 8, y + h - 40), (x + w - 8, y + h - 40),
                  (x + w - 34, y + h - 14), (x + 30, y + h - 14)],
                 fill=(178, 52, 44))
    # containers
    draw.rectangle([x + 26, y + 18, x + 76, y + h - 40], fill=OCHRE)
    draw.rectangle([x + 82, y + 30, x + 128, y + h - 40], fill=TEAL)
    # funnel
    draw.rectangle([x + w - 62, y + 6, x + w - 30, y + h - 40], fill=NAVY)
    # explosion burst top right
    bx, by = x + w - 30, y - 6
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x2 = bx + 26 * math.cos(a)
        y2 = by + 26 * math.sin(a)
        draw.line([(bx, by), (x2, y2)], fill=(230, 140, 30), width=5)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(230, 140, 30))


def icon_city_drone(draw, x, y, w, h):
    # skyline (kept inside the 150px icon box so it never touches the text)
    base = y + h - 16
    buildings = [(0, 55), (28, 92), (56, 44), (84, 78), (112, 52)]
    for bx, bh in buildings:
        draw.rectangle([x + bx, base - bh, x + bx + 24, base], fill=NAVY)
    # windows
    for bx, bh in buildings:
        for wy in range(base - bh + 10, base - 8, 18):
            draw.rectangle([x + bx + 6, wy, x + bx + 11, wy + 7], fill=(240, 200, 90))
    # drone, top-left of the icon box
    dx, dy = x + 26, y + 12
    draw.ellipse([dx - 10, dy - 6, dx + 10, dy + 6], fill=INK)
    for sx in (-22, 22):
        draw.ellipse([dx + sx - 8, dy - 8, dx + sx + 8, dy + 8],
                     outline=INK, width=3)
        draw.line([(dx, dy), (dx + sx, dy)], fill=INK, width=3)
    # dashed path
    for i in range(6):
        yy = dy + 26 + i * 12
        draw.line([(dx - 4, yy), (dx + 4, yy)], fill=RED, width=3)


def icon_badge(draw, cx, cy, r):
    # shield
    draw.polygon([(cx, cy - r), (cx + r, cy - r * 0.45), (cx + r * 0.8, cy + r * 0.6),
                  (cx, cy + r), (cx - r * 0.8, cy + r * 0.6),
                  (cx - r, cy - r * 0.45)], fill=OCHRE, outline=INK, width=3)
    # star
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = r * 0.5 if i % 2 == 0 else r * 0.22
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=PAPER)


def icon_warship(draw, x, y, w, h):
    # a corvette listing to starboard, bow up, stern going under;
    # kept inside the 150px icon box so it never touches the text
    # smoke above the stern
    for (sx, sy, sr) in [(x + 24, y + 58, 10), (x + 40, y + 46, 13),
                         (x + 56, y + 56, 9)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 146, 138))
    # hull, bow high on the right, stern low on the left
    draw.polygon([(x + 14, y + 76), (x + 118, y + 46), (x + 130, y + 56),
                  (x + 30, y + 94)], fill=(70, 80, 92))
    # deck edge
    draw.line([(x + 14, y + 76), (x + 118, y + 46)], fill=(150, 156, 164),
              width=3)
    # superstructure and mast near the bow
    draw.rectangle([x + 88, y + 40, x + 106, y + 55], fill=(120, 126, 134))
    draw.line([(x + 97, y + 40), (x + 97, y + 28)], fill=INK, width=3)
    # gun turret and barrel at the bow
    draw.rectangle([x + 104, y + 40, x + 116, y + 50], fill=(120, 126, 134))
    draw.line([(x + 116, y + 44), (x + 130, y + 38)], fill=INK, width=4)
    # explosion burst at the bow waterline
    bx, by = x + 132, y + 50
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x2 = bx + 22 * math.cos(a)
        y2 = by + 22 * math.sin(a)
        draw.line([(bx, by), (x2, y2)], fill=(230, 140, 30), width=5)
    draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(230, 140, 30))
    # sea
    for i in range(3):
        yy = y + h - 22 + i * 9
        draw.arc([x, yy - 8, x + w, yy + 8], 0, 180, fill=NAVY, width=3)


# ------------------------------------------------------------------ page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 38  # margin
    CW = W - 2 * M  # content width

    # ---- masthead
    y = 30
    kicker(d, M, y, "MONDAY  •  23 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE")
    y += 30
    f_title = font(SERIF_B, 74)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, y), title, font=f_title, fill=INK)
    y += 92
    rule(d, M, y, CW, INK, 4)
    y += 6
    rule(d, M, y, CW, INK, 1)
    y += 14

    # ---- lead story: COP31 (full width)
    lead_y = y
    lead_h = 250
    d.rectangle([M, lead_y, W - M, lead_y + lead_h], fill=LIGHT,
                outline=INK, width=2)
    # illustration left
    icon_globe(d, M + 130, lead_y + 142, 72)
    # kicker + headline right
    tx = M + 268
    twd = W - M - 24 - tx
    kicker(d, tx, lead_y + 18, "CLIMATE  •  LEAD STORY", size=20)
    hy = draw_wrapped(d, (tx, lead_y + 48), "COP31 CLIMATE TALKS COLLAPSE",
                      font(SERIF_B, 46), twd, leading=52)
    draw_wrapped(d, (tx, hy + 6),
                 "Nations fail to agree on fossil fuels, the UN chief is "
                 "“deeply disappointed” as the summit ends in disarray.",
                 font(SANS, 23), twd, leading=29)
    y = lead_y + lead_h + 18

    # ---- row 2: two half panels
    row_h = 200
    half = (CW - 16) // 2
    panels = [
        ("STRAIT OF HORMUZ", "TANKERS HIT AS GULF CONFLICT WIDENS",
         "Two tankers hit on Saturday as the Gulf conflict widens.",
         "tanker"),
        ("UKRAINE", "DRONE STRIKE HITS KYIV",
         "At least 12 killed in overnight strikes on the Kyiv region.",
         "city"),
    ]
    for i, (kick, head, dek, kind) in enumerate(panels):
        x = M + i * (half + 16)
        d.rectangle([x, y, x + half, y + row_h], fill=PAPER,
                    outline=INK, width=2)
        ix, iy = x + 14, y + 44
        if kind == "tanker":
            icon_tanker(d, ix, iy, 150, 120)
        else:
            icon_city_drone(d, ix, iy, 150, 120)
        tx2 = x + 178
        tw2 = x + half - 14 - tx2
        kicker(d, tx2, y + 14, kick, size=17)
        hy2 = draw_wrapped(d, (tx2, y + 40), head, font(SERIF_B, 27), tw2,
                           leading=31)
        draw_wrapped(d, (tx2, hy2 + 4), dek, font(SANS, 19), tw2, leading=24)
    y += row_h + 18

    # ---- row 3: two half panels
    panels = [
        ("MEXICO", "CARTEL BOSS CAPTURED",
         "FBI-wanted “Chapo Isidro” seized in Sinaloa; 11 killed in the firefight.",
         "badge"),
        ("LIBYA", "RUSSIAN WARSHIP SUNK OFF LIBYA",
         "Kyiv confirms sea drones sank the corvette Merkury.",
         "warship"),
    ]
    for i, (kick, head, dek, kind) in enumerate(panels):
        x = M + i * (half + 16)
        d.rectangle([x, y, x + half, y + row_h], fill=PAPER,
                    outline=INK, width=2)
        if kind == "badge":
            icon_badge(d, x + 88, y + 112, 62)
        else:
            icon_warship(d, x + 14, y + 44, 150, 120)
        tx2 = x + 178
        tw2 = x + half - 14 - tx2
        kicker(d, tx2, y + 14, kick, size=17)
        hy2 = draw_wrapped(d, (tx2, y + 40), head, font(SERIF_B, 27), tw2,
                           leading=31)
        draw_wrapped(d, (tx2, hy2 + 4), dek, font(SANS, 19), tw2, leading=24)
    y += row_h + 18

    # ---- also-today strip
    strip_y = y
    strip_h = 92
    d.rectangle([M, strip_y, W - M, strip_y + strip_h], fill=NAVY)
    draw_wrapped(d, (M + 16, strip_y + 12),
                 "ALSO TODAY:  Democrats win 258 House seats, biggest since 1992  •  "
                 "Riemann proof confirmed  •  South Korea exports pass $1 trillion  •  "
                 "Denmark: Russia plotted to kill rapper Kyivstoner  •  "
                 "AI fears sink markets: Nikkei -5.06%, S&P -3.7%",
                 font(SANS_B, 19), CW - 32, fill=(246, 241, 231), leading=25)
    y = strip_y + strip_h + 14

    # ---- footer
    rule(d, M, y, CW, INK, 1)
    f_foot = font(SANS, 17)
    foot = "23 NOVEMBER 2026  •  THE DAY’S WORLD NEWS, IN ONE IMAGE"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, y + 8), foot, font=f_foot, fill=GREY)

    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = main()
    img.save(out, "PNG", optimize=True)
    print(out, img.size)
