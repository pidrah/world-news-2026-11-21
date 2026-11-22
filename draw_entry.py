#!/usr/bin/env python3
"""Draws the bounty entry image: one poster summing up 21 November 2026's world news.

Rendered at 2x (2048x2048) and downscaled to 1024x1024 for clean edges.
Events sourced from Wikipedia's Current events portal for 2026-11-21 (accessed 22 Nov 2026).
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample factor
W = H = 1024 * S

# ---------- palette ----------
PAPER   = (247, 242, 231)   # cream newsprint
INK     = (26, 34, 56)      # dark navy ink
NAVY    = (21, 29, 51)
RED     = (192, 57, 43)     # masthead accent
GOLD    = (230, 179, 62)
WHITE   = (255, 255, 255)
GREY    = (110, 116, 130)
LIGHT   = (233, 226, 210)   # panel border on paper

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, size * S)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- helpers ----------
def text_w(draw, s, font):
    b = draw.textbbox((0, 0), s, font=font)
    return b[2] - b[0]

def wrap(draw, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(draw, t, font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def para(draw, xy, s, font, maxw, fill, lh=None, align="left", maxlines=None):
    lines = wrap(draw, s, font, maxw)
    if maxlines and len(lines) > maxlines:
        lines = lines[:maxlines]
        lines[-1] = lines[-1].rsplit(" ", 1)[0] + "…" if " " in lines[-1] else lines[-1]
    x, y = xy
    lh = lh or int(font.size * 1.15)
    for ln in lines:
        if align == "center":
            draw.text((x - text_w(draw, ln, font) // 2, y), ln, font=font, fill=fill)
        else:
            draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y
# ---------- masthead (0..150) ----------
MH = 150 * S
d.rectangle([0, 0, W, MH], fill=NAVY)
d.rectangle([0, MH, W, MH + 6 * S], fill=RED)
para(d, (W // 2, 18 * S), "THE DAY IN PICTURES", F("DejaVuSans-Bold.ttf", 17), W, GOLD, align="center")
para(d, (W // 2, 46 * S), "WORLD NEWS", F("DejaVuSerif-Bold.ttf", 58), W, WHITE, align="center")
para(d, (W // 2, 120 * S), "SATURDAY 21 NOVEMBER 2026", F("DejaVuSans-Bold.ttf", 24), W, PAPER, align="center")

# ---------- panel grid ----------
TOP = MH + 6 * S
GRID_H = 890 * S - TOP          # leave 1024-890=134 for ticker
COLS, ROWS = 2, 3
GAP = 10 * S
MARG = 12 * S
PW = (W - MARG * 2 - GAP) // COLS
PH = (GRID_H - GAP * (ROWS - 1)) // ROWS

def panel(r, c, draw_fn, kicker, headline, sub, accent):
    x0 = MARG + c * (PW + GAP)
    y0 = TOP + r * (PH + GAP)
    d.rectangle([x0, y0, x0 + PW, y0 + PH], fill=WHITE, outline=LIGHT, width=S)
    IW = int(PW * 0.36)
    d.rectangle([x0, y0, x0 + IW, y0 + PH], fill=(250, 247, 239))
    draw_fn(x0, y0, IW, PH)
    tx = x0 + IW + 12 * S
    tw = x0 + PW - tx - 10 * S
    y = y0 + 10 * S
    para(d, (tx, y), kicker, F("DejaVuSans-Bold.ttf", 13), tw, accent)
    y += 19 * S
    y = para(d, (tx, y), headline, F("DejaVuSans-Bold.ttf", 21), tw, INK, lh=25 * S, maxlines=3)
    y += 3 * S
    d.line([tx, y, tx + tw, y], fill=LIGHT, width=S)
    y += 4 * S
    para(d, (tx, y), sub, F("DejaVuSans.ttf", 14), tw, GREY, lh=17 * S, maxlines=4)



# ----- 1. BepiColombo at Mercury (science / space) -----
def icon_mercury(x0, y0, iw, ih):
    cx, cy = x0 + iw // 2, y0 + ih // 2 + 6 * S
    d.ellipse([cx - 44 * S, cy - 44 * S, cx + 44 * S, cy + 44 * S], fill=(176, 138, 112), outline=(120, 92, 74), width=2 * S)
    for ox, oy, r in [(-16, -14, 9), (14, 6, 12), (-4, 22, 7), (22, -20, 6), (-26, 8, 5)]:
        d.ellipse([cx + ox * S - r * S, cy + oy * S - r * S, cx + ox * S + r * S, cy + oy * S + r * S], fill=(146, 112, 90))
    d.ellipse([cx - 78 * S, cy - 30 * S, cx + 78 * S, cy + 30 * S], outline=GOLD, width=2 * S)
    sx, sy = cx - 74 * S, cy - 12 * S
    d.rectangle([sx - 5 * S, sy - 4 * S, sx + 5 * S, sy + 4 * S], fill=NAVY)
    d.rectangle([sx - 16 * S, sy - 2 * S, sx - 6 * S, sy + 2 * S], fill=(58, 110, 189))
    d.rectangle([sx + 6 * S, sy - 2 * S, sx + 16 * S, sy + 2 * S], fill=(58, 110, 189))
    d.line([sx, sy, sx, sy - 8 * S], fill=NAVY, width=S)
panel(0, 0, icon_mercury, "SPACE", "BepiColombo enters orbit at Mercury",
      "ESA announces its probe reached the innermost planet", (58, 110, 189))

# ----- 2. Gaza aid truck strike -----
def icon_gaza(x0, y0, iw, ih):
    gy = y0 + ih - 52 * S
    d.rectangle([x0 + iw * 0.28, gy, x0 + iw * 0.62, gy + 20 * S], fill=WHITE, outline=INK, width=2 * S)
    d.rectangle([x0 + iw * 0.62, gy + 6 * S, x0 + iw * 0.74, gy + 20 * S], fill=INK)
    d.ellipse([x0 + iw * 0.33 - 5 * S, gy + 18 * S, x0 + iw * 0.33 + 5 * S, gy + 28 * S], fill=INK)
    d.ellipse([x0 + iw * 0.60 - 5 * S, gy + 18 * S, x0 + iw * 0.60 + 5 * S, gy + 28 * S], fill=INK)
    ux, uy = x0 + iw * 0.5, y0 + 26 * S
    d.rectangle([ux - 10 * S, uy - 3 * S, ux + 10 * S, uy + 3 * S], fill=INK)
    d.line([ux - 18 * S, uy - 8 * S, ux - 6 * S, uy], fill=INK, width=2 * S)
    d.line([ux + 18 * S, uy - 8 * S, ux + 6 * S, uy], fill=INK, width=2 * S)
    d.line([ux, uy + 3 * S, ux, gy + 8 * S], fill=RED, width=2 * S)
    for a in range(0, 360, 45):  # impact burst at ground
        bx, by = ux, gy + 8 * S
        d.line([bx, by, bx + 9 * S * math.cos(math.radians(a)), by + 9 * S * math.sin(math.radians(a))], fill=RED, width=2 * S)
panel(0, 1, icon_gaza, "GAZA", "Israeli drone strike hits food truck",
      "Four Palestinians killed in Gaza City and Jabalia", (146, 43, 33))

# ----- 3. Gulf of Finland ship -----
def icon_ship(x0, y0, iw, ih):
    wy = y0 + ih - 44 * S
    hx, hy = x0 + iw * 0.2, wy - 34 * S
    d.polygon([(hx, hy + 22 * S), (hx + iw * 0.6, hy + 22 * S), (hx + iw * 0.52, hy + 34 * S), (hx + 8 * S, hy + 34 * S)], fill=(58, 110, 189))
    d.rectangle([hx + 6 * S, hy - 4 * S, hx + iw * 0.54, hy + 22 * S], fill=NAVY)
    for i in range(4):
        d.rectangle([hx + 12 * S + i * 18 * S, hy + 2 * S, hx + 24 * S + i * 18 * S, hy + 12 * S], fill=(214, 222, 235))
    d.rectangle([hx + iw * 0.44, hy - 16 * S, hx + iw * 0.47, hy - 4 * S], fill=INK)
    fx, fy = hx + iw * 0.3, hy - 6 * S
    d.polygon([(fx - 7 * S, fy), (fx, fy - 16 * S), (fx + 7 * S, fy), (fx, fy + 6 * S)], fill=(226, 92, 32))
    d.polygon([(fx - 3 * S, fy), (fx, fy - 8 * S), (fx + 3 * S, fy)], fill=GOLD)
    for i, off in enumerate([-8, 0, 8]):
        d.arc([x0 + 14 * S + i * 8 * S, wy + off * S, x0 + iw - 14 * S + i * 8 * S, wy + 26 * S + off * S],
              200, 340, fill=(58, 110, 189), width=2 * S)
panel(1, 0, icon_ship, "BALTIC SEA", "Drone hits cargo ship in Gulf of Finland",
      "Fire on Russian vessel; Finland restricts airspace", (36, 90, 160))

# ----- 4. Riyadh interceptions -----
def icon_riyadh(x0, y0, iw, ih):
    by = y0 + ih - 40 * S
    bx = x0 + iw * 0.5
    d.rectangle([bx - 26 * S, by - 64 * S, bx + 26 * S, by], fill=NAVY)
    d.ellipse([bx - 26 * S, by - 84 * S, bx + 26 * S, by - 52 * S], fill=NAVY)
    d.rectangle([bx - 8 * S, by - 96 * S, bx + 8 * S, by - 84 * S], fill=NAVY)
    d.rectangle([bx - 58 * S, by - 34 * S, bx - 34 * S, by], fill=(72, 82, 110))
    d.rectangle([bx + 34 * S, by - 26 * S, bx + 58 * S, by], fill=(72, 82, 110))
    for i, dx in enumerate([-40, 0, 40]):
        mx = bx + dx * S
        d.line([mx, y0 + 18 * S, mx - 6 * S, y0 + 40 * S], fill=RED, width=2 * S)
        d.line([mx - 6 * S, y0 + 40 * S, mx, y0 + 62 * S], fill=RED, width=2 * S)
        cx, cy = mx - 3 * S, y0 + 44 * S
        d.line([cx - 8 * S, cy - 8 * S, cx + 8 * S, cy + 8 * S], fill=GOLD, width=3 * S)
        d.line([cx - 8 * S, cy + 8 * S, cx + 8 * S, cy - 8 * S], fill=GOLD, width=3 * S)
panel(1, 1, icon_riyadh, "SAUDI ARABIA", "Three Houthi missiles intercepted at Riyadh",
      "Saudi defences shoot down missiles aimed at the capital", (154, 112, 28))

# ----- 5. Bangladesh garment strike -----
def icon_factory(x0, y0, iw, ih):
    by = y0 + ih - 38 * S
    fx = x0 + iw * 0.16
    d.rectangle([fx, by - 44 * S, fx + iw * 0.62, by], fill=WHITE, outline=INK, width=2 * S)
    for i in range(3):
        sx = fx + i * (iw * 0.62) / 3
        d.polygon([(sx, by - 44 * S), (sx + (iw * 0.62) / 3 * 0.8, by - 66 * S), (sx + (iw * 0.62) / 3 * 0.8, by - 44 * S)], fill=NAVY)
    for i in range(3):
        d.rectangle([fx + 10 * S + i * 24 * S, by - 30 * S, fx + 20 * S + i * 24 * S, by - 16 * S], fill=GREY)
    hx, hy = x0 + iw * 0.8, by - 30 * S
    d.rectangle([hx - 9 * S, hy, hx + 9 * S, hy + 30 * S], fill=(196, 132, 92))
    d.rounded_rectangle([hx - 8 * S, hy - 26 * S, hx + 8 * S, hy + 2 * S], 6 * S, fill=(196, 132, 92))
    d.line([hx, hy - 40 * S, hx, hy - 24 * S], fill=RED, width=3 * S)
    d.line([hx - 10 * S, hy - 36 * S, hx - 7 * S, hy - 23 * S], fill=RED, width=2 * S)
    d.line([hx + 10 * S, hy - 36 * S, hx + 7 * S, hy - 23 * S], fill=RED, width=2 * S)
panel(2, 0, icon_factory, "BANGLADESH", "Garment strike shuts 80 factories",
      "Wage protests in Savar and Ashulia; 96 arrested", (146, 90, 26))

# ----- 6. Indonesia–EU trade deal -----
def icon_trade(x0, y0, iw, ih):
    cy = y0 + ih // 2
    ex, ey = x0 + iw * 0.26, cy
    d.ellipse([ex - 30 * S, ey - 30 * S, ex + 30 * S, ey + 30 * S], fill=(28, 60, 140))
    for a in range(0, 360, 45):
        sx = ex + 18 * S * math.cos(math.radians(a))
        sy = ey + 18 * S * math.sin(math.radians(a))
        star = [(sx + 4 * S * math.cos(math.radians(90 + k * 72)), sy - 4 * S * math.sin(math.radians(90 + k * 72))) for k in range(5)]
        star += [(sx + 2 * S * math.cos(math.radians(126 + k * 72)), sy - 2 * S * math.sin(math.radians(126 + k * 72))) for k in range(5)]
        d.polygon(star, fill=GOLD)
    ix_, iy_ = x0 + iw * 0.74, cy
    d.ellipse([ix_ - 30 * S, iy_ - 30 * S, ix_ + 30 * S, iy_ + 30 * S], fill=WHITE, outline=LIGHT, width=2 * S)
    d.pieslice([ix_ - 30 * S, iy_ - 30 * S, ix_ + 30 * S, iy_ + 30 * S], 180, 360, fill=RED)
    d.line([ex + 34 * S, cy, ix_ - 40 * S, cy], fill=INK, width=3 * S)
    d.polygon([(ix_ - 40 * S, cy - 7 * S), (ix_ - 40 * S, cy + 7 * S), (ix_ - 28 * S, cy)], fill=INK)
panel(2, 1, icon_trade, "INDONESIA – EU", "Trade and investment deals signed",
      "98.5% of tariffs on EU goods to be lifted", (28, 60, 140))

# ---------- ticker (bottom band) ----------
TK = 890 * S
d.rectangle([0, TK, W, H], fill=NAVY)
d.rectangle([0, TK, W, TK + 4 * S], fill=GOLD)
para(d, (W // 2, TK + 16 * S), "ALSO ON 21 NOVEMBER 2026", F("DejaVuSans-Bold.ttf", 15), W, GOLD, align="center")
para(d, (24 * S, TK + 48 * S),
     "BASRA, IRAQ: power-station fire kills four, injures 35   •   SERANG, INDONESIA: candy-factory fire, three dead and 36 missing   •   JAPAN–SAUDI ARABIA: oil stored in Japan to triple to 24 million barrels",
     F("DejaVuSans.ttf", 15), W - 48 * S, PAPER, lh=20 * S)

# ---------- finish: downscale and save ----------
out = img.resize((1024, 1024), Image.LANCZOS)
out.save("/home/thee2/.cline/data/workspaces/chat/makefun-news-image/entry.png", optimize=True)
print("saved", out.size)

